from abc import ABC, abstractmethod


class DataEncoder(ABC):
    """
    A helper to unify encoding/decoding from string to bytes and vice versa.
    """

    @abstractmethod
    def encode(self, content: str) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> str:
        pass
