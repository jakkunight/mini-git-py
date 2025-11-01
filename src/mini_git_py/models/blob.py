from dataclasses import dataclass
from mini_git_py.models.git_objects import GitObject


@dataclass
class Blob:
    name: str
    mode: int
    content: bytes
    type = "blob"

    def __post_init__(self):
        pass

    def to_git_object(self) -> GitObject:
        return GitObject(sha, self.type, size, self.content)
