from abc import ABC, abstractmethod
from typing import override
from ..object_values import Sha256Hash
from pathlib import Path


class ObjectPathBuilder(ABC):
    """
    A dependency that builds a Path from a Sha256Hash.
    """

    @abstractmethod
    def build_object_path(self, sha: Sha256Hash) -> Path:
        pass

    @abstractmethod
    def exists(self, sha: Sha256Hash) -> bool:
        pass


class LocalObjectPathBuilder(ObjectPathBuilder):
    """Constructor de rutas para objetos locales"""

    _base_dir: Path

    def __init__(self, base_dir: Path):
        self._base_dir = base_dir

    @override
    def build_object_path(self, sha: Sha256Hash) -> Path:
        # Similar a Git: primeros 2 caracteres como directorio, resto como nombre
        sha_str = sha.sha
        return self._base_dir / sha_str[:32] / sha_str[32:]

    @override
    def exists(self, sha: Sha256Hash) -> bool:
        return self.build_object_path(sha).exists()
