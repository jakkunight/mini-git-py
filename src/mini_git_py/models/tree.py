from mini_git_py.models.git_objects import GitObject, GitObjectType
from hashlib import sha256


class TreeEntry:
    def __init__(self, dirname: str):
        self.mode = "040000"
        self.dirname = dirname


class BlobEntry:
    def __init__(self, filename: str):
        self.mode = "100644"
        self.filename = filename


class Tree(GitObject):
    def __init__(self, blob_entries: list[BlobEntry], tree_entries: list[TreeEntry]):
        self.tree_entries = tree_entries
        self.blob_entries = blob_entries

    def get_content(self) -> str:
        content_str: str = ""
        separator: str = "\n"
        inner_separator: str = " "

        content_str += self.get_type()
        content_str += separator

        for entry in self.tree_entries:
            content_str += entry.mode
            content_str += inner_separator
            content_str += entry.dirname
            content_str += separator

        for entry in self.blob_entries:
            content_str += entry.mode
            content_str += inner_separator
            content_str += entry.filename
            content_str += separator

        return content_str

    def compute_hash(self) -> str:
        content: str = self.get_content()

        content_bytes: bytes = content.encode("utf-8")
        hash = sha256(content_bytes)

        hex_str: str = hash.hexdigest()

        return hex_str

    def get_type(self) -> GitObjectType:
        return GitObjectType.TREE
