from abc import ABC, abstractmethod

from models.blob import Blob
from models.hash import Sha256Hash


class BlobRepository(ABC):
    @abstractmethod
    def save_blob(self, blob: Blob) -> Sha256Hash | None:
        pass

    @abstractmethod
    def load_blob(self, sha: Sha256Hash) -> Blob:
        pass
