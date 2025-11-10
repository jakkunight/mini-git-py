from abc import ABC, abstractmethod

from models.commit import Commit
from models.hash import Sha256Hash


class CommitRepository(ABC):
    @abstractmethod
    def save_commit(self, commit: Commit) -> str | None:
        pass

    @abstractmethod
    def load_commit(self, sha: Sha256Hash) -> Commit | None:
        pass
