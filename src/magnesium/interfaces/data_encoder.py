from abc import ABC, abstractmethod
from typing import override


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


class Utf8Encoder(DataEncoder):
    """Codificador que usa UTF-8"""

    @override
    def encode(self, content: str) -> bytes:
        return content.encode("utf-8")

    @override
    def decode(self, data: bytes) -> str:
        return data.decode("utf-8")
