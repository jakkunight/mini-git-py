from abc import ABC, abstractmethod
from models import Sha256Hash
from pathlib import Path


class ObjectPathBuilder(ABC):
    """
    A dependency that builds a Path from a Sha256Hash.
    """

    @abstractmethod
    def build_object_path(self, sha: Sha256Hash) -> Path:
        pass
