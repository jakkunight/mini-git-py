from abc import ABC, abstractmethod

from models import Diff


class Differ(ABC):
    @abstractmethod
    def diff_text_lines(self, base: list[str], target: list[str]) -> Diff | None:
        pass
