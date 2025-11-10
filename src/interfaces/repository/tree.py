from abc import ABC, abstractmethod

from models.hash import Sha256Hash
from models.tree import Tree


class TreeRepository(ABC):
    @abstractmethod
    def save_tree(self, tree: Tree) -> Sha256Hash | None:
        pass

    @abstractmethod
    def load_tree(self, sha: Sha256Hash) -> Tree | None:
        pass
