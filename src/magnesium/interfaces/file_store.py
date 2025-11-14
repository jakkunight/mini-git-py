from abc import ABC, abstractmethod
from pathlib import Path
from typing import override


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

    @abstractmethod
    def delete(self, path: Path):
        pass


class LocalFileStore(FileStore):
    """Almacenamiento en sistema de archivos local"""

    @override
    def write(self, path: Path, data: bytes):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            _ = f.write(data)

    @override
    def read(self, path: Path) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    @override
    def delete(self, path: Path):
        path.unlink()


class WorkingDirectory(FileStore):
    def __init__(self):
        pass

    @override
    def write(self, path: Path, data: bytes):
        return super().write(path, data)

    @override
    def read(self, path: Path) -> bytes:
        return super().read(path)

    @override
    def delete(self, path: Path):
        return super().delete(path)
