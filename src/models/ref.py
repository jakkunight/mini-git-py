from dataclasses import dataclass

from models.hash import Sha256Hash


@dataclass
class CommitRef:
    name: str
    sha: Sha256Hash

    def __post_init__(self):
        try:
            assert self.name is not None, (
                "El nombre de la referencia no puede estar vacío."
            )
        except Exception as e:
            print(e)


@dataclass
class TagRef:
    name: str
    sha: Sha256Hash

    def __post_init__(self):
        try:
            assert self.name is not None, (
                "El nombre de la referencia no puede estar vacío."
            )
        except Exception as e:
            print(e)
