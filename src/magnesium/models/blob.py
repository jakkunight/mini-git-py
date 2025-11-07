from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Blob:
    name: str
    mode: int
    content: bytes

    
    type = "blob"

    def __post_init__(self) -> None:
        assert self.name != ""

        assert isinstance(self.mode, int)

        assert self.mode >= 0

        assert isinstance(
            self.content, (bytes, bytearray, memoryview)
        ) 

        if isinstance(self.content, (bytearray, memoryview)):
           
            self.content = bytes(self.content)


__all__ = ["Blob"]