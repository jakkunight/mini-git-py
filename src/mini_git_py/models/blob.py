from dataclasses import dataclass


@dataclass
class Blob:
    name: str
    mode: int
    content: bytes
    type = "blob"

    def __post_init__(self):
        pass
