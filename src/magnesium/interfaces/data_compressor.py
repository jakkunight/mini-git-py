from abc import ABC, abstractmethod


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
