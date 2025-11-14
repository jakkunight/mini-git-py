from abc import ABC, abstractmethod
from typing import override

from ..object_values import (
    AddedDirEntry,
    AddedFileEntry,
    DeletedDirEntry,
    DeletedFileEntry,
    FileEntry,
    DirEntry,
    Tree,
    UnchangedDirEntry,
    UnchangedFileEntry,
)
from ..object_values.blob import Blob
from ..object_values.diffs import (
    AddedLine,
    BlobDiff,
    DeletedLine,
    TreeDiff,
    UnchangedLine,
)


class Differ(ABC):
    """
    An object that finds the diffs between Blobs and Trees.
    """

    @abstractmethod
    def diff_blobs(self, base: Blob, source: Blob) -> BlobDiff:
        pass

    @abstractmethod
    def diff_trees(self, base: Tree, source: Tree) -> TreeDiff:
        pass


class MyersDiff(Differ):
    """
    Implementación del algoritmo de Myers para calcular diferencias
    entre blobs y trees.
    """

    def __init__(self) -> None:
        pass

    @override
    def diff_blobs(self, base: Blob, source: Blob) -> BlobDiff:
        base_lines = base.get_lines()
        source_lines = source.get_lines()
        path = self._myers_algorithm(base_lines, source_lines)
        return self._build_blob_diff_from_path(path, base_lines, source_lines)

    @override
    def diff_trees(self, base: Tree, source: Tree) -> TreeDiff:
        """
        Calcula la diferencia entre dos árboles comparando directorios y archivos.
        """
        return TreeDiff(
            added_files=self._find_added_files(base.files, source.files),
            deleted_files=self._find_deleted_files(base.files, source.files),
            unchanged_files=self._find_unchanged_files(base.files, source.files),
            added_dirs=self._find_added_dirs(base.directories, source.directories),
            deleted_dirs=self._find_deleted_dirs(base.directories, source.directories),
            unchanged_dirs=self._find_unchanged_dirs(
                base.directories, source.directories
            ),
        )

    def _myers_algorithm(
        self, a: list[str], b: list[str]
    ) -> list[tuple[int, int, str]]:
        """
        Implementación del algoritmo de Myers para encontrar el camino de edición más corto.

        Returns:
            Lista de tuplas (x, y, operation) donde operation puede ser:
            'delete', 'insert', or 'equal'
        """
        n, m = len(a), len(b)
        max_ = n + m

        # V array para el algoritmo
        v = [0] * (2 * max_ + 1)
        v[1] = 0

        # Almacenar historial para reconstrucción
        trace: list[list[int]] = []

        for d in range(0, max_ + 1):
            trace.append(v[:])

            for k in range(-d, d + 1, 2):
                # Decidir si movernos hacia abajo o hacia la derecha
                if k == -d or (k != d and v[k - 1 + max_] < v[k + 1 + max_]):
                    x = v[k + 1 + max_]
                else:
                    x = v[k - 1 + max_] + 1

                y = x - k

                # Avanzar en diagonales mientras las líneas sean iguales
                while x < n and y < m and a[x] == b[y]:
                    x += 1
                    y += 1

                v[k + max_] = x

                # Si llegamos al final, terminamos
                if x >= n and y >= m:
                    return self._build_path(trace, a, b)

        return []

    def _build_path(
        self, trace: list[list[int]], a: list[str], b: list[str]
    ) -> list[tuple[int, int, str]]:
        """
        Reconstruye el camino desde el trace del algoritmo de Myers.
        """
        n, m = len(a), len(b)
        x, y = n, m
        path: list[tuple[int, int, str]] = []
        max_ = len(trace[0]) // 2

        for d in range(len(trace) - 1, -1, -1):
            v = trace[d]
            k = x - y

            if k == -d or (k != d and v[k - 1 + max_] < v[k + 1 + max_]):
                prev_k = k + 1
                # operation = "insert"
            else:
                prev_k = k - 1
                # operation = "delete"

            prev_x = v[prev_k + max_]
            prev_y = prev_x - prev_k

            # Agregar operaciones no diagonales
            while x > prev_x and y > prev_y:
                path.append((x - 1, y - 1, "equal"))
                x -= 1
                y -= 1

            if x > prev_x:
                path.append((x - 1, y, "delete"))
                x -= 1
            elif y > prev_y:
                path.append((x, y - 1, "insert"))
                y -= 1

        return list(reversed(path))

    def _build_blob_diff_from_path(
        self,
        path: list[tuple[int, int, str]],
        base_lines: list[str],
        source_lines: list[str],
    ) -> BlobDiff:
        """
        Construye un BlobDiff desde el camino generado por Myers.
        """
        additions: list[AddedLine] = []
        deletions: list[DeletedLine] = []
        unchanged: list[UnchangedLine] = []

        current_position = 0

        for x, y, operation in path:
            if operation == "equal":
                unchanged.append(
                    UnchangedLine(position=current_position, content=base_lines[x])
                )
                current_position += 1
            elif operation == "delete":
                deletions.append(
                    DeletedLine(position=current_position, content=base_lines[x])
                )
                # En delete, no avanzamos la posición porque removemos
            elif operation == "insert":
                additions.append(
                    AddedLine(position=current_position, content=source_lines[y])
                )
                current_position += 1

        return BlobDiff(
            additions=additions, deletions=deletions, unchanged_lines=unchanged
        )

    def _find_added_files(
        self, base_files: list[FileEntry], source_files: list[FileEntry]
    ) -> list[AddedFileEntry]:
        """Encuentra archivos añadidos."""
        base_names = {f.name for f in base_files}
        return [AddedFileEntry(f) for f in source_files if f.name not in base_names]

    def _find_deleted_files(
        self, base_files: list[FileEntry], source_files: list[FileEntry]
    ) -> list[DeletedFileEntry]:
        """Encuentra archivos eliminados."""
        source_names = {f.name for f in source_files}
        return [DeletedFileEntry(f) for f in base_files if f.name not in source_names]

    def _find_unchanged_files(
        self, base_files: list[FileEntry], source_files: list[FileEntry]
    ) -> list[UnchangedFileEntry]:
        """Encuentra archivos sin cambios."""
        source_file_map = {f.name: f for f in source_files}
        unchanged = []

        for base_file in base_files:
            if base_file.name in source_file_map:
                source_file = source_file_map[base_file.name]
                # Considerar unchanged si tienen el mismo nombre y SHA
                if (
                    base_file.name == source_file.name
                    and base_file.sha == source_file.sha
                ):
                    unchanged.append(UnchangedFileEntry(base_file))

        return unchanged

    def _find_added_dirs(
        self, base_dirs: list[DirEntry], source_dirs: list[DirEntry]
    ) -> list[AddedDirEntry]:
        """Encuentra directorios añadidos."""
        base_names = {d.name for d in base_dirs}
        return [AddedDirEntry(d) for d in source_dirs if d.name not in base_names]

    def _find_deleted_dirs(
        self, base_dirs: list[DirEntry], source_dirs: list[DirEntry]
    ) -> list[DeletedDirEntry]:
        """Encuentra directorios eliminados."""
        source_names = {d.name for d in source_dirs}
        return [DeletedDirEntry(d) for d in base_dirs if d.name not in source_names]

    def _find_unchanged_dirs(
        self, base_dirs: list[DirEntry], source_dirs: list[DirEntry]
    ) -> list[UnchangedDirEntry]:
        """Encuentra directorios sin cambios."""
        source_dir_map = {d.name: d for d in source_dirs}
        unchanged = []

        for base_dir in base_dirs:
            if base_dir.name in source_dir_map:
                source_dir = source_dir_map[base_dir.name]
                if base_dir.name == source_dir.name and base_dir.sha == source_dir.sha:
                    unchanged.append(UnchangedDirEntry(base_dir))

        return unchanged
