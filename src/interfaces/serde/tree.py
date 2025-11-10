from abc import ABC, abstractmethod
from models.tree import Tree


class TreeSerializer(ABC):
    @abstractmethod
    def serialize_tree(self, tree: Tree) -> str:
        pass

    @abstractmethod
    def deserialize_tree(self, data: str) -> Tree:
        pass
