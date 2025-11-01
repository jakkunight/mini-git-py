from dataclasses import dataclass


@dataclass
class Tag:
    name: str
    type = "tag"

    def __post_init__(self):
        pass
