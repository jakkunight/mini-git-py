from dataclasses import dataclass
from datetime import datetime

from models.hash import Sha256Hash
from models.email import Email


@dataclass
class Commit:
    author: str
    email: Email
    message: str
    date: datetime
    tree: Sha256Hash
    parents: list[Sha256Hash]

    def __post_init__(self):
        try:
            assert self.author is not None, "El nombre del autor no puede estar vacío."
            assert self.message is not None, "El mensaje provisto no puede estar vacío."
        except Exception as e:
            print(e)
