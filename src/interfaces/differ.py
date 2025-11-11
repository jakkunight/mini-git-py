from abc import ABC, abstractmethod

from models import Blob, BlobDiff, Tree, TreeDiff


class Differ(ABC):
    @abstractmethod
    def diff_blobs(self, base: Blob, source: Blob) -> BlobDiff | None:
        pass

    @abstractmethod
    def diff_trees(self, base: Tree, source: Tree) -> TreeDiff | None:
        pass
