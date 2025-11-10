from abc import ABC, abstractmethod
from models.blob import Blob


class BlobSerializer(ABC):
    @abstractmethod
    def serialize_blob(self, blob: Blob) -> str:
        pass

    @abstractmethod
    def deserialize_blob(self, data: str) -> Blob:
        pass
