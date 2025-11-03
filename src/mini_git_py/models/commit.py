from datetime import datetime, timezone
from mini_git_py.models.author import Author
from mini_git_py.models.git_objects import GitObject, GitObjectType
from hashlib import sha256


class Commit(GitObject):
    def __init__(self, author: Author, message: str, tree_hash: str, parent_hash: str):
        if message == "" or message is None:
            raise TypeError("No se puede asignar un mensaje vacío a un commit.")
        if tree_hash == "" or tree_hash is None:
            raise TypeError("Tree Hash inválido.")
        if parent_hash == "" or parent_hash is None:
            raise TypeError("Parent Hash inválido.")
        self.author: Author = author
        self.date = str(datetime.now(timezone.utc))
        self.message = message
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash

    def get_type(self) -> GitObjectType:
        return GitObjectType.COMMIT

    def get_content(self) -> str:
        separator: str = "\n"
        content_str: str = ""

        content_str += self.get_type()
        content_str += separator

        content_str += "Author: " + self.author.name
        content_str += separator
        content_str += "Email: " + self.author.email
        content_str += separator
        content_str += "Date: " + self.date
        content_str += separator
        content_str += "Message: " + self.message
        content_str += separator
        content_str += "Tree: " + self.tree_hash
        content_str += separator
        content_str += "Parent: " + self.parent_hash

        return content_str

    def compute_hash(self) -> str:
        content: str = self.get_content()
        content_bytes: bytes = content.encode("utf-8")
        hash = sha256(content_bytes)
        hex_str = hash.hexdigest()
        return hex_str
