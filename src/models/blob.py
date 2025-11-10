from dataclasses import dataclass


@dataclass
class Blob:
    content: str

    def __post_init__(self):
        pass
