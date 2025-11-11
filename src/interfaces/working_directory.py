from abc import ABC, abstractmethod
from pathlib import Path

from models import Email, Sha256Hash, Tree


class WorkingDirectory(ABC):
    @abstractmethod
    def init(self, path: Path) -> Path | None:
        pass

    @abstractmethod
    def stage_files(self, paths: list[Path]) -> Tree | None:
        pass

    @abstractmethod
    def stage_file(self, path: Path) -> Tree | None:
        pass

    @abstractmethod
    def stage_dir(self, path: Path) -> Tree | None:
        pass

    @abstractmethod
    def commit(self, author: str, email: Email, message: str) -> Sha256Hash | None:
        pass

    @abstractmethod
    def checkout_commit(self, commit: Sha256Hash) -> Tree | None:
        pass

    @abstractmethod
    def checkout_ref(self, ref: str) -> Tree | None:
        pass

    @abstractmethod
    def checkout_tag(self, tag: str) -> Tree | None:
        pass
