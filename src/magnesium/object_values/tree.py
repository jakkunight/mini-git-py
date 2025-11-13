from dataclasses import dataclass

from .hash import Sha256Hash


@dataclass
class DirEntry:
    name: str
    mode: int
    sha: Sha256Hash


@dataclass
class FileEntry:
    name: str
    mode: int
    sha: Sha256Hash


@dataclass
class Tree:
    directories: list[DirEntry]
    files: list[FileEntry]
