from dataclasses import dataclass
import re


@dataclass
class TreeEntry:
    """
    Una clase que representa una entrada de tipo 'blob' de un directorio.
    """

    mode: int
    name: str
    sha: str

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """

        assert re.match(r"^[a-f0-9]{64}$", self.sha), """
            El hash ingresado es inválido.
        """


@dataclass
class BlobEntry:
    """
    Una clase que representa una entrada de tipo 'blob' de un directorio.
    """

    mode: int
    name: str
    sha: str

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """

        assert re.match(r"^[a-f0-9]{64}$", self.sha), """
            El hash ingresado es inválido.
        """


@dataclass
class Tree:
    """
    Una clase que representa a las entradas de un directorio.
    """

    tree_entries: list[TreeEntry]
    blob_entries: list[BlobEntry]
    type: str = "tree"

    def __post_init__(self):
        assert self.blob_entries != [] or self.tree_entries != [], """
            El árbol provisto no puede estar vacío. Debe contener al menos una entrada.
        """
