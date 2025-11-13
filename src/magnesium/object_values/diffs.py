from dataclasses import dataclass

from .tree import DirEntry, FileEntry


@dataclass
class DeletedLine:
    position: int
    content: str

    def __post_init__(self):
        try:
            assert self.position >= 0
        except Exception as e:
            print(e)


@dataclass
class AddedLine:
    position: int
    content: str

    def __post_init__(self):
        try:
            assert self.position >= 0
        except Exception as e:
            print(e)


@dataclass
class UnchangedLine:
    position: int
    content: str

    def __post_init__(self):
        try:
            assert self.position >= 0
        except Exception as e:
            print(e)


@dataclass
class DeletedFileEntry:
    content: FileEntry

    def __post_init__(self):
        pass


@dataclass
class AddedFileEntry:
    content: FileEntry

    def __post_init__(self):
        pass


@dataclass
class UnchangedFileEntry:
    content: FileEntry

    def __post_init__(self):
        pass


@dataclass
class DeletedDirEntry:
    content: DirEntry

    def __post_init__(self):
        pass


@dataclass
class AddedDirEntry:
    content: DirEntry

    def __post_init__(self):
        pass


@dataclass
class UnchangedDirEntry:
    content: DirEntry

    def __post_init__(self):
        pass


@dataclass
class BlobDiff:
    additions: list[AddedLine]
    deletions: list[DeletedLine]
    unchanged_lines: list[UnchangedLine]

    def __post_init__(self):
        assert (
            self.additions != [] or self.deletions != [] or self.unchanged_lines != []
        )


@dataclass
class TreeDiff:
    added_files: list[AddedFileEntry]
    deleted_files: list[DeletedFileEntry]
    unchanged_files: list[UnchangedFileEntry]
    added_dirs: list[AddedDirEntry]
    deleted_dirs: list[DeletedDirEntry]
    unchanged_dirs: list[UnchangedDirEntry]

    def __post_init__(self):
        assert (
            self.added_dirs != []
            or self.added_files != []
            or self.deleted_dirs != []
            or self.deleted_files != []
            or self.unchanged_dirs != []
            or self.unchanged_files != []
        )
