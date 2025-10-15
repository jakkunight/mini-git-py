from hashlib import sha256
from author import Author


class Commit:
    def __init__(
        self, author: Author, tree: int, message: str, previous_commit_hash: int
    ):
        self.author = author
        self.tree = tree
        self.message = message
        self.previous_commit_hash = previous_commit_hash
