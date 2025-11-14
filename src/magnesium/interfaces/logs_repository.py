from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

from magnesium.interfaces.data_encoder import DataEncoder
from ..object_values import Sha256Hash, Commit
from .file_store import FileStore
from .object_path_builder import ObjectPathBuilder
from .object_repository import ObjectRepository


class LogRepository(ABC):
    """
    An interface to log the commit history.
    """

    @abstractmethod
    def push(self, sha: Sha256Hash):
        pass

    @abstractmethod
    def load(self) -> list[Commit]:
        pass

    @abstractmethod
    def search(self, sha: Sha256Hash) -> Commit:
        pass

    @abstractmethod
    def exists(self, sha: Sha256Hash) -> bool:
        pass

    @abstractmethod
    def pop(self, sha: Sha256Hash | None = None) -> Commit:
        pass


class LocalLogRepository(LogRepository):
    _base_path: Path
    _encoder: DataEncoder
    _file_store: FileStore
    _path_builder: ObjectPathBuilder
    _repository: ObjectRepository

    def __init__(
        self,
        base_path: Path,
        file_store: FileStore,
        encoder: DataEncoder,
        path_builder: ObjectPathBuilder,
        repository: ObjectRepository,
    ) -> None:
        self._base_path = base_path
        self._file_store = file_store
        self._encoder = encoder
        self._path_builder = path_builder
        self._repository = repository

        # Asegurar que el directorio base existe
        self._base_path.mkdir(parents=True, exist_ok=True)

    @override
    def exists(self, sha: Sha256Hash) -> bool:
        # Verificar que el commit existe en el repositorio de objetos
        if not self._repository.exists(sha):
            return False

        # Además, verificar que está en el log
        log_entries = self._load_log_entries()
        for _, child in log_entries:
            if child == sha.sha:
                return True
        return False

    @override
    def search(self, sha: Sha256Hash) -> Commit:
        # Primero verificar que existe en el log
        if not self.exists(sha):
            raise KeyError(f"Commit {sha.sha} not found in log")

        # Cargar el commit desde el repositorio de objetos
        result = self._repository.load(sha)
        if not isinstance(result, Commit):
            raise ValueError(f"Object {sha.sha} is not a Commit")
        return result

    @override
    def push(self, sha: Sha256Hash):
        # Verificar que el sha corresponde a un commit válido
        if not self._repository.exists(sha):
            raise ValueError(f"Hash {sha.sha} does not correspond to any object")

        result = self._repository.load(sha)
        if not isinstance(result, Commit):
            raise ValueError(f"Object {sha.sha} is not a Commit")

        # Cargar las entradas existentes del log
        log_entries = self._load_log_entries()

        if not log_entries:
            # Primer commit: (root, nuevo_commit)
            log_entries.append(("root", sha.sha))
        else:
            # Encontrar el último commit (el que no tiene hijo)
            last_commit = self._find_last_commit(log_entries)
            # Agregar nuevo commit como hijo del último
            log_entries.append((last_commit, sha.sha))

        # Guardar el log actualizado
        self._save_log_entries(log_entries)

    @override
    def pop(self, sha: Sha256Hash | None = None) -> Commit:
        log_entries = self._load_log_entries()

        if not log_entries:
            raise IndexError("Cannot pop from empty log")

        if sha is None:
            # Eliminar el último commit (el que no tiene hijo)
            last_commit_sha = self._find_last_commit(log_entries)

            # Encontrar y eliminar la entrada que tiene este commit como hijo
            entry_to_remove = None
            for entry in log_entries:
                if entry[1] == last_commit_sha:
                    entry_to_remove = entry
                    break

            if entry_to_remove:
                log_entries.remove(entry_to_remove)
                removed_commit = self.search(Sha256Hash(last_commit_sha))
                self._save_log_entries(log_entries)
                return removed_commit
            else:
                raise ValueError("Could not find last commit in log")
        else:
            # Eliminar un commit específico
            # Esto es más complejo porque rompe la cadena
            entry_to_remove = None
            for entry in log_entries:
                if entry[1] == sha.sha:
                    entry_to_remove = entry
                    break

            if not entry_to_remove:
                raise KeyError(f"Commit {sha.sha} not found in log")

            # Encontrar el padre y el hijo del commit a eliminar
            parent_entry = entry_to_remove
            child_entry = None
            for entry in log_entries:
                if entry[0] == sha.sha:
                    child_entry = entry
                    break

            # Reconectar la cadena si hay un hijo
            if child_entry:
                # Reemplazar: (padre -> este) y (este -> hijo) por (padre -> hijo)
                log_entries.remove(parent_entry)
                log_entries.remove(child_entry)
                log_entries.append((parent_entry[0], child_entry[1]))
            else:
                # Solo eliminar la entrada si es el último
                log_entries.remove(parent_entry)

            removed_commit = self.search(sha)
            self._save_log_entries(log_entries)
            return removed_commit

    @override
    def load(self) -> list[Commit]:
        log_entries = self._load_log_entries()
        commits: list[Commit] = []

        # Reconstruir el orden cronológico
        commit_order = self._get_commit_order(log_entries)

        for commit_sha in commit_order:
            try:
                commit = self.search(Sha256Hash(commit_sha))
                commits.append(commit)
            except (KeyError, ValueError) as e:
                print(f"Warning: Could not load commit {commit_sha}: {e}")
                continue

        return commits

    def get_head(self) -> Sha256Hash | None:
        """Obtener el último commit (HEAD)"""
        log_entries = self._load_log_entries()
        if not log_entries:
            return None

        last_commit_sha = self._find_last_commit(log_entries)
        return Sha256Hash(last_commit_sha)

    def _load_log_entries(self) -> list[tuple[str, str]]:
        """Cargar todas las entradas del log"""
        log_file = self._base_path / "logfile"

        if not log_file.exists():
            return []

        try:
            encoded_log = self._file_store.read(log_file)
            serialized_log = self._encoder.decode(encoded_log)

            # Eliminar el separador final si existe
            serialized_log = serialized_log.rstrip("\x1e")

            if not serialized_log:
                return []

            log_lines = serialized_log.split("\x1e")
            logs: list[tuple[str, str]] = []

            for line in log_lines:
                if line.strip():
                    parent, child = line.split("\x1f")
                    logs.append((parent, child))

            return logs

        except Exception as e:
            print(f"Warning: Could not load log file: {e}")
            return []

    def _save_log_entries(self, log_entries: list[tuple[str, str]]):
        """Guardar las entradas del log"""
        serialized_log = ""
        for parent, child in log_entries:
            serialized_log += f"{parent}\x1f{child}\x1e"

        encoded_log = self._encoder.encode(serialized_log)
        self._file_store.write(self._base_path / "logfile", encoded_log)

    def _find_last_commit(self, log_entries: list[tuple[str, str]]) -> str:
        """Encontrar el último commit (el que no es padre de nadie)"""
        # Colectar todos los padres
        parents = set(entry[0] for entry in log_entries)

        # Encontrar el commit que no es padre de nadie
        for entry in log_entries:
            if entry[1] not in parents:
                return entry[1]

        # Si todos los commits son padres de alguien, hay un ciclo (error)
        raise ValueError("Circular reference detected in log")

    def _get_commit_order(self, log_entries: list[tuple[str, str]]) -> list[str]:
        """Obtener el orden cronológico de los commits"""
        if not log_entries:
            return []

        # Construir el orden desde el primero hasta el último
        commit_order: list[str] = []

        # Encontrar el primer commit (el que tiene "root" como padre)
        first_commit = None
        for entry in log_entries:
            if entry[0] == "root":
                first_commit = entry[1]
                break

        if not first_commit:
            raise ValueError("No root commit found in log")

        # Seguir la cadena
        current_commit = first_commit
        visited: set[str] = set()

        while current_commit and current_commit not in visited:
            visited.add(current_commit)
            commit_order.append(current_commit)

            # Encontrar el siguiente commit
            next_commit = None
            for entry in log_entries:
                if entry[0] == current_commit:
                    next_commit = entry[1]
                    break

            current_commit = next_commit

        return commit_order
