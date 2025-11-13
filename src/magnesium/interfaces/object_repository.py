from abc import ABC, abstractmethod
from datetime import datetime
from hashlib import sha256
from os import makedirs
from pathlib import Path
from typing import override
from ..object_values import Blob, Commit, DirEntry, Email, FileEntry, Sha256Hash, Tree
from .object_path_builder import ObjectPathBuilder
from .data_compressor import DataCompressor
from .data_encoder import DataEncoder
from .file_store import FileStore


class ObjectRepository(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def exists(self, sha: Sha256Hash) -> bool:
        pass

    @abstractmethod
    def hash_object(self, object: Blob | Tree | Commit) -> Sha256Hash:
        pass

    @abstractmethod
    def save(self, object: Blob | Tree | Commit) -> Sha256Hash:
        pass

    @abstractmethod
    def load(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        pass

    @abstractmethod
    def delete(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        pass


class LocalObjectRepository(ObjectRepository):
    _store: FileStore
    _encoder: DataEncoder
    _compressor: DataCompressor
    _path_builder: ObjectPathBuilder
    _base_path: Path
    # Caracteres de control ASCII para separación
    UNIT_SEPARATOR: str = "\x1e"  # ASCII US (Unit Separator)
    RECORD_SEPARATOR: str = "\x1f"  # ASCII RS (Record Separator)
    GROUP_SEPARATOR: str = "\x1d"  # ASCII GS (Group Separator)

    def __init__(
        self,
        base_path: Path,
        store: FileStore,
        encoder: DataEncoder,
        compressor: DataCompressor,
        path_builder: ObjectPathBuilder,
    ) -> None:
        self._store = store
        self._path_builder = path_builder
        self._encoder = encoder
        self._compressor = compressor
        self._base_path = base_path

    @override
    def init(self):
        makedirs(self._base_path / ".mg")

    @override
    def exists(self, sha: Sha256Hash) -> bool:
        object_path = self._path_builder.build_object_path(sha)
        return object_path.exists()

    @override
    def hash_object(self, object: Blob | Tree | Commit) -> Sha256Hash:
        content = ""
        if isinstance(object, Blob):
            encoded_blob = self._encoder.encode(object.content)
            content = f"blob{self.UNIT_SEPARATOR}{len(encoded_blob)}{self.GROUP_SEPARATOR}{encoded_blob}"
        elif isinstance(object, Tree):
            content = f"tree{self.UNIT_SEPARATOR}"
            body = ""
            for entry in object.directories:
                body += f"tree{self.UNIT_SEPARATOR}{entry.mode}{self.UNIT_SEPARATOR}{entry.sha.sha}{self.UNIT_SEPARATOR}{entry.name}{self.RECORD_SEPARATOR}"
            body += self.GROUP_SEPARATOR
            for entry in object.files:
                body += f"blob{self.UNIT_SEPARATOR}{entry.mode}{self.UNIT_SEPARATOR}{entry.sha.sha}{self.UNIT_SEPARATOR}{entry.name}{self.RECORD_SEPARATOR}"
            encoded_body = self._encoder.encode(body)
            content += f"{len(encoded_body)}{self.GROUP_SEPARATOR}{encoded_body}"
        else:
            body = f"{object.author}{self.UNIT_SEPARATOR}{object.email.email}{self.UNIT_SEPARATOR}{object.date.isoformat()}{self.UNIT_SEPARATOR}{object.message}{self.UNIT_SEPARATOR}{object.tree.sha}{self.UNIT_SEPARATOR}"
            for parent in object.parents:
                body += f"{parent.sha}{self.UNIT_SEPARATOR}"
            encoded_body = self._encoder.encode(body)
            content = f"commit{self.UNIT_SEPARATOR}{len(encoded_body)}{self.GROUP_SEPARATOR}{encoded_body}"
        encoded_content = self._encoder.encode(content)
        hexdigest = sha256(encoded_content).hexdigest()
        hash = Sha256Hash(hexdigest)
        return hash

    @override
    def save(self, object: Blob | Tree | Commit) -> Sha256Hash:
        # Calcular el hash del objeto
        object_hash = self.hash_object(object)

        # Si el objeto ya existe, no hacer nada
        if self.exists(object_hash):
            return object_hash

        # Construir el contenido según el formato especificado
        if isinstance(object, Blob):
            # Header: type + US + size
            header = f"blob{self.UNIT_SEPARATOR}{len(object.content)}"
            # Body: contenido directo
            body = object.content
            # Contenido final: header + GS + body
            content = f"{header}{self.GROUP_SEPARATOR}{body}"

        elif isinstance(object, Tree):
            # Construir el body con entradas separadas por RS
            body_parts: list[str] = []

            # Directorios
            for dir_entry in object.directories:
                entry_str = f"tree{self.UNIT_SEPARATOR}{dir_entry.mode}{self.UNIT_SEPARATOR}{dir_entry.sha.sha}{self.UNIT_SEPARATOR}{dir_entry.name}"
                body_parts.append(entry_str)

            # Files
            for file_entry in object.files:
                entry_str = f"blob{self.UNIT_SEPARATOR}{file_entry.mode}{self.UNIT_SEPARATOR}{file_entry.sha.sha}{self.UNIT_SEPARATOR}{file_entry.name}"
                body_parts.append(entry_str)

            # Unir todas las entradas con RS
            body = self.RECORD_SEPARATOR.join(body_parts)

            # Header: type + US + tamaño del body
            header = f"tree{self.UNIT_SEPARATOR}{len(body)}"
            # Contenido final: header + GS + body
            content = f"{header}{self.GROUP_SEPARATOR}{body}"

        else:  # Commit
            # Construir el body con campos separados por US
            body_parts = [
                object.author,
                object.email.email,
                object.date.isoformat(),
                object.message,
                object.tree.sha,
            ]

            # Agregar padres
            for parent in object.parents:
                body_parts.append(parent.sha)

            # Unir campos con US
            body = self.UNIT_SEPARATOR.join(body_parts)

            # Header: type + US + tamaño del body
            header = f"commit{self.UNIT_SEPARATOR}{len(body)}"
            # Contenido final: header + GS + body
            content = f"{header}{self.GROUP_SEPARATOR}{body}"

        # Codificar, comprimir y guardar
        encoded_content = self._encoder.encode(content)
        compressed_content = self._compressor.compress(encoded_content)

        object_path = self._path_builder.build_object_path(object_hash)
        self._store.write(object_path, compressed_content)

        return object_hash

    @override
    def load(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        if not self.exists(sha):
            raise FileNotFoundError(f"Object with hash {sha.sha} not found")

        # Obtener la ruta y leer el contenido
        object_path = self._path_builder.build_object_path(sha)
        compressed_content = self._store.read(object_path)

        # Descomprimir y decodificar
        encoded_content = self._compressor.decompress(compressed_content)
        content = self._encoder.decode(encoded_content)

        # Parsear el contenido según el formato: header + GS + body
        gs_pos = content.find(self.GROUP_SEPARATOR)
        if gs_pos == -1:
            raise ValueError("Invalid object format: missing group separator")

        header = content[:gs_pos]
        body = content[gs_pos + 1 :]

        # Parsear header: type + US + size
        us_pos = header.find(self.UNIT_SEPARATOR)
        if us_pos == -1:
            raise ValueError("Invalid header format: missing unit separator")

        type_name = header[:us_pos]
        size_str = header[us_pos + 1 :]

        # Verificar que el tamaño coincida
        expected_size = int(size_str)
        if len(body) != expected_size:
            raise ValueError(
                f"Size mismatch: expected {expected_size}, got {len(body)}"
            )

        # Parsear según el tipo
        if type_name == "blob":
            return Blob(content=body)

        elif type_name == "tree":
            directories: list[DirEntry] = []
            files: list[FileEntry] = []

            # Dividir las entradas por RS
            entries = body.split(self.RECORD_SEPARATOR) if body else []

            for entry_str in entries:
                if not entry_str.strip():
                    continue

                # Parsear cada entrada: type + US + mode + US + sha + US + name
                parts = entry_str.split(self.UNIT_SEPARATOR)
                if len(parts) != 4:
                    raise ValueError(f"Invalid tree entry format: {entry_str}")

                entry_type, mode_str, sha_hex, name = parts

                mode = int(mode_str)
                sha_obj = Sha256Hash(sha_hex)

                if entry_type == "tree":
                    directories.append(DirEntry(name=name, mode=mode, sha=sha_obj))
                elif entry_type == "blob":
                    files.append(FileEntry(name=name, mode=mode, sha=sha_obj))
                else:
                    raise ValueError(f"Unknown tree entry type: {entry_type}")

            return Tree(directories=directories, files=files)

        elif type_name == "commit":
            # Dividir campos por US
            parts = body.split(self.UNIT_SEPARATOR)
            if len(parts) < 5:
                raise ValueError("Invalid commit format: insufficient fields")

            author, email_str, date_str, message, tree_sha, *parent_shas = parts

            # Parsear fecha
            try:
                date = datetime.fromisoformat(date_str)
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}")

            # Construir lista de padres
            parents = [Sha256Hash(sha) for sha in parent_shas if sha.strip()]

            return Commit(
                author=author,
                email=Email(email_str),
                message=message,
                date=date,
                tree=Sha256Hash(tree_sha),
                parents=parents,
            )

        else:
            raise ValueError(f"Unknown object type: {type_name}")

    @override
    def delete(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        if not self.exists(sha):
            raise FileNotFoundError(f"Object with hash {sha.sha} not found")

        # Cargar el objeto primero para devolverlo
        object = self.load(sha)

        # Eliminar el archivo
        object_path = self._path_builder.build_object_path(sha)
        self._store.delete(object_path)

        return object
