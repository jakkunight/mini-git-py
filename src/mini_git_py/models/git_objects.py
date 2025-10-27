from abc import ABC, abstractmethod
from enum import Enum


class GitObjectType(Enum):
    BLOB = "blob"
    TREE = "tree"
    COMMIT = "commit"


class GitObject(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def compute_hash(self) -> str:
        return ""

    @abstractmethod
    def get_type(self) -> GitObjectType:
        return GitObjectType.BLOB

    @abstractmethod
    def get_content(self) -> str:
        return ""
