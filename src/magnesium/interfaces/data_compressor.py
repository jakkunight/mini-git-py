from abc import ABC, abstractmethod
from typing import override
import gzip


class DataCompressor(ABC):
    """
    A dependency that compresses/decompresses some bytes using a unified format.
    """

    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        pass


class GzipCompressor(DataCompressor):
    """Compresor usando gzip"""

    @override
    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data)

    @override
    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)
