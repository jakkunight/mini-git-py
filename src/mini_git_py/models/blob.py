from mini_git_py.models.git_objects import GitObject, GitObjectType
from hashlib import sha256


class Blob(GitObject):
    def __init__(self, content: str):
        self.content = content

    def compute_hash(self) -> str:
        content: str = self.get_content()
        content_bytes: bytes = content.encode("utf-8")
        hash = sha256(content_bytes)
        hex_str = hash.hexdigest()
        return hex_str

    def get_type(self) -> GitObjectType:
        return GitObjectType.BLOB

    def get_content(self) -> str:
        separator: str = "\n"
        content_str: str = ""

        content_str += self.get_type()
        content_str += separator
        content_size: int = len(self.content.encode("utf-8"))
        content_str += "Size: " + str(content_size)
        content_str += separator + separator
        content_str += self.content

        return content_str
