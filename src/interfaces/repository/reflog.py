from abc import ABC, abstractmethod

from models.hash import Sha256Hash
from models.reflog import Reflog


class ReflogRepository(ABC):
    @abstractmethod
    def load_reflogs(self, ref_name: str) -> Reflog | None:
        pass

    @abstractmethod
    def save_reflogs(self, ref_name: str) -> Sha256Hash | None:
        pass
