from dataclasses import dataclass
import re


@dataclass
class Commit:
    """
    Una clase que representa un commit. Un commit es un snapshot inmutable del estado del working directory en una fecha concreta.
    """

    author: str
    email: str
    message: str
    date: str
    parents: list[str]
    tree: str
    type: str = "commit"

    def __post_init__(self):
        assert self.author != "", """
            El nombre del autor no puede estar vacío.
        """
        assert re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email
        ), """
            El email ingresado es inválido.
        """
        assert self.message != "", """
            El mensaje no puede estar vacío.
        """
        for parent in self.parents:
            assert re.match(r"^[a-f0-9]{64}$", parent), """
                El commit anterior ingresado es inválido.
            """

        assert re.match(r"^[a-f0-9]{64}$", self.tree), """
            El tree ingresado es inválido.
        """
        assert self.type == "commit", """
            El tipo de dato debe ser siempre "commit" y no debe ser modificado!
        """

    def add_parent(self, parent: str):
        assert len(self.parents) <= 2, """
            No se pueden asignar más commits padre al commit actual.
            Sólo puede haber hasta dos commits padres por commit.
        """
        assert re.match(r"^[a-f0-9]{64}$", parent), """
            El commit anterior ingresado es inválido.
        """

        self.parents.append(parent)
