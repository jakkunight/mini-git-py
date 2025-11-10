from abc import ABC, abstractmethod


class DataEncoder(ABC):
    @abstractmethod
    def encode(self, data: str) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> str:
        pass
