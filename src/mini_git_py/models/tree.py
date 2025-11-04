from dataclasses import dataclass
import re


@dataclass
class TreeEntry:
    mode: int
    name: str
    sha: str
    obj_type: str

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """

        assert re.match(r"^[a-f0-9]{64}$", self.sha), """
            El tree ingresado es inválido.
        """

        assert self.obj_type in ("blob", "tree"), """
            El tipo debe ser "blob" o "tree".
        """


@dataclass
class Tree:
    name: str
    type = "tree"
    entries: list[TreeEntry]

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede ser vacío.
        """

    def add_entry(self, entry: TreeEntry):
        self.entries.append(entry)
