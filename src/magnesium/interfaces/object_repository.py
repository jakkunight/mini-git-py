from abc import ABC, abstractmethod
from models import Blob, Commit, Sha256Hash, Tree


# NOTE:
# Tag support is not going to be implemented.
class ObjectRepository(ABC):
    @abstractmethod
    def exists(self, sha: Sha256Hash) -> bool:
        pass

    @abstractmethod
    def hash_object(self, object: Blob | Tree | Commit) -> Sha256Hash:
        pass

    @abstractmethod
    def save(self, object: Blob | Tree | Commit) -> Sha256Hash:
        pass

    @abstractmethod
    def load(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        pass

    @abstractmethod
    def delete(self, sha: Sha256Hash) -> Blob | Tree | Commit:
        pass
