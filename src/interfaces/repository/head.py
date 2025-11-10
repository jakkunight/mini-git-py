from abc import ABC, abstractmethod

from models.hash import Sha256Hash
from models.ref import CommitRef


class RepositoryHead(ABC):
    @abstractmethod
    def update_head(self, ref: CommitRef) -> Sha256Hash:
        pass

    @abstractmethod
    def load_head(self) -> CommitRef:
        pass
