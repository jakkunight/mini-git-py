from abc import ABC, abstractmethod

from models.ref import CommitRef, TagRef


class RefRepository(ABC):
    @abstractmethod
    def save_tag_ref(self, ref: TagRef) -> str | None:
        pass

    @abstractmethod
    def load_tag_ref(self, name: str) -> TagRef | None:
        pass

    @abstractmethod
    def save_commit_ref(self, ref: CommitRef) -> str | None:
        pass

    @abstractmethod
    def load_commit_ref(self, name: str) -> CommitRef | None:
        pass
