from mini_git_py.models.git_objects import GitObject
import re


class Commit:
    author: str
    email: str
    message: str
    type = "commit"
    date: str
    parents: list[str | None]
    tree: str

    def __init__(self, author: str, email: str, message: str, parent: str, tree: str):
        assert author != "", """
            El nombre del autor no puede estar vacío.
        """
        assert re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email), """
            El email ingresado es inválido.
        """
        assert message != "", """
            El mensaje no puede estar vacío.
        """
        assert re.match(r"^[a-f0-9]{64}$", parent), """
            El commit anterior ingresado es inválido.
        """
        assert re.match(r"^[a-f0-9]{64}$", tree), """
            El tree ingresado es inválido.
        """

        self.author = author
        self.email = email
        self.parents: list[str | None] = [parent]
        self.tree = tree

    def add_parent(self, parent: str):
        assert len(self.parents) <= 2, """
            No se pueden asignar más commits padre al commit actual.
            Sólo puede haber hasta dos commits padres por commit.
        """
        assert re.match(r"^[a-f0-9]{64}$", parent), """
            El commit anterior ingresado es inválido.
        """

        self.parents.append(parent)

    def build_content(self) -> bytes:
        buffer = f"tree {self.tree}\n"
        for parent in self.parents:
            buffer += f"parent {parent}\n"
        buffer += f"author {self.author}\n"
        buffer += f"email {self.email}\n"

        self.content = buffer

        return bytes(buffer)

    def compute_hash(self):
        pass
