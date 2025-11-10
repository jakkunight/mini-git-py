from abc import ABC, abstractmethod
from pathlib import Path


class FileStore(ABC):
    @abstractmethod
    def save(self, path: Path, data: bytes) -> int | None:
        pass

    @abstractmethod
    def load(self, path: Path) -> bytes | None:
        pass
