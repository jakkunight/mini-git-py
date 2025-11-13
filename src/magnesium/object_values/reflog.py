from dataclasses import dataclass

from .hash import Sha256Hash


@dataclass
class Reflog:
    log: list[Sha256Hash]

    def __post_init__(self):
        pass
