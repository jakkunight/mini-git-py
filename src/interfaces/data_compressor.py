from abc import ABC, abstractmethod


class DataCompressor(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes | None:
        pass

    @abstractmethod
    def decompress(self, data: bytes) -> bytes | None:
        pass
