from dataclasses import dataclass
from datetime import datetime

from models.email import Email
from models.hash import Sha256Hash


@dataclass
class Tag:
    title: str
    body: str
    commit: Sha256Hash
    author: str
    email: Email
    date: datetime

    def __post_init__(self):
        try:
            assert self.author is not None, "El nombre del autor no puede estar vacío."
            assert self.title is not None, (
                "El título del tag provisto no puede estar vacío."
            )
            assert self.body is not None, "El mensaje provisto no puede estar vacío."
        except Exception as e:
            print(e)
