from abc import ABC, abstractmethod

from models.hash import Sha256Hash
from models.tree import Tree


class IndexRepository(ABC):
    @abstractmethod
    def save_index(self, index: Tree) -> Sha256Hash | None:
        pass

    @abstractmethod
    def load_index(self) -> Tree | None:
        pass
