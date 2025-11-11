from dataclasses import dataclass


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
class Diff:
    additions: list[AddedLine]
    deletions: list[DeletedLine]
    unchanged_lines: list[UnchangedLine]

    def __post_init__(self):
        assert (
            self.additions != [] or self.deletions != [] or self.unchanged_lines != []
        )
