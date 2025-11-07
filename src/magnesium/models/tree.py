from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable


@dataclass
class TreeEntry:
    

    mode: int
    name: str
    sha: str
    obj_type: str

    def __post_init__(self) -> None:
     assert isinstance(self.mode, int) 

     assert self.name != ""

     assert re.fullmatch(r"[a-f0-9]{64}", self.sha) 

     assert self.obj_type in ("blob", "tree")


@dataclass
class Tree:
    

    name: str
    entries: list[TreeEntry] | Iterable[TreeEntry] = field(default_factory=list)

    
    type = "tree"
    

    def __post_init__(self) -> None:
        assert self.name != ""

    
        if not isinstance(self.entries, list):
            self.entries = list(self.entries)

        for entry in self.entries:
            assert isinstance(entry, TreeEntry)

        self.entries.sort(key=lambda entry: entry.name)

    def add_entry(self, entry: TreeEntry) -> None:
        assert isinstance(entry, TreeEntry)
        self.entries.append(entry)
        self.entries.sort(key=lambda item: item.name)


__all__ = ["Tree", "TreeEntry"]