from dataclasses import dataclass
import re


@dataclass
class Commit:
    author: str
    email: str
    message: str
    type = "commit"
    date: str
    parents: list[str | None]
    tree: str

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
            if parent is None:
                continue
            assert re.match(r"^[a-f0-9]{64}$", parent), """
                El commit anterior ingresado es inválido.
            """

        assert re.match(r"^[a-f0-9]{64}$", self.tree), """
            El tree ingresado es inválido.
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
