from abc import ABC, abstractmethod


class FileStore(ABC):
    """
    A class to read/write bytes from the disk. It just reads raw bytes.
    In write mode, OVERWRITES THE SPECIFIED FILE.
    """

    @abstractmethod
    def write(self, path: Path, data: bytes):
        pass

    @abstractmethod
    def read(self, path: Path) -> bytes:
        pass
