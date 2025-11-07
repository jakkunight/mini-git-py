from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

from mini_git_py.models.blob import Blob
from mini_git_py.models.repository import Repository
from mini_git_py.models.tree import Tree, TreeEntry

IGNORED_DIRECTORIES: frozenset[str] = frozenset({".mg"})


@dataclass(frozen=True)
class TreeBuildResult:
    tree: Tree
    sha: str


class TreeBuilder:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def build_from_path(self, path: str | Path) -> TreeBuildResult:
        
        root_path = Path(path).resolve()
        if not root_path.exists():
            raise AssertionError(
                f"La ruta provista no existe.\n\nValor provisto:\n- {root_path}"
            )
        if not root_path.is_dir():
            raise AssertionError(
                f"Se esperaba una carpeta para construir un Tree.\n\nRuta recibida:\n- {root_path}"
            )

        tree, sha = self._build_tree(root_path, ".")
        if self._repository.update_index(tree) is None:
            raise AssertionError("No se pudo actualizar el índice del repositorio.")
        return TreeBuildResult(tree=tree, sha=sha)

    def _build_tree(self, directory: Path, tree_name: str) -> Tuple[Tree, str]:
        entries = []
        for entry in self._iter_directory(directory):
            stat_result = entry.stat()
            if entry.is_dir():
                child_tree, child_sha = self._build_tree(entry, entry.name)
                entries.append(
                    TreeEntry(
                        mode=stat_result.st_mode,
                        name=entry.name,
                        sha=child_sha,
                        obj_type="tree",
                    )
                )
            elif entry.is_file():
                blob_sha = self._save_blob(entry, stat_result.st_mode)
                entries.append(
                    TreeEntry(
                        mode=stat_result.st_mode,
                        name=entry.name,
                        sha=blob_sha,
                        obj_type="blob",
                    )
                )
        tree = Tree(name=tree_name, entries=entries)
        tree_sha = self._repository.save_tree(tree)
        if tree_sha is None:
            raise AssertionError(
                f"No se pudo guardar el Tree correspondiente a: {directory}"
            )
        return tree, tree_sha

    def _iter_directory(self, directory: Path) -> Iterable[Path]:
        for entry in sorted(directory.iterdir(), key=lambda path: path.name):
            if entry.name in IGNORED_DIRECTORIES:
                continue
            yield entry

    def _save_blob(self, file_path: Path, mode: int) -> str:
        with file_path.open("rb") as handle:
            content = handle.read()
        blob = Blob(
            name=file_path.name,
            mode=mode,
            content=content,
        )
        sha = self._repository.save_blob(blob)
        if sha is None:
            raise AssertionError(
                f"No se pudo guardar el blob correspondiente a: {file_path}"
            )
        return sha


def build_tree(repository: Repository, path: str | Path) -> TreeBuildResult:
    return TreeBuilder(repository).build_from_path(path)


__all__ = ["TreeBuilder", "TreeBuildResult", "build_tree"]