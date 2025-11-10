from abc import ABC, abstractmethod

from models.hash import Sha256Hash
from models.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    def save_tag(self, tag: Tag) -> Sha256Hash | None:
        pass

    @abstractmethod
    def load_tag(self, sha: Sha256Hash) -> Tag | None:
        pass
