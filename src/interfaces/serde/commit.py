from abc import ABC, abstractmethod

from models.commit import Commit


class CommitSerializer(ABC):
    @abstractmethod
    def serialize_commit(self, commit: Commit) -> str:
        pass

    @abstractmethod
    def deserialize_commit(self, data: str) -> Commit:
        pass
