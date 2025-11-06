from dataclasses import dataclass
import re


@dataclass
class TreeEntry:
    """
    Una clase que representa una entrada de un directorio.
    """

    mode: int
    name: str
    sha: str
    obj_type: str

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """

        assert re.match(r"^[a-f0-9]{64}$", self.sha), """
            El hash ingresado es inválido.
        """

        assert self.obj_type in ("blob", "tree"), """
            El tipo debe ser "blob" o "tree".
        """


@dataclass
class Tree:
    """
    Una clase que representa a las entradas de un directorio.
    """

    name: str
    type = "tree"
    entries: list[TreeEntry]

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede ser vacío.
        """
