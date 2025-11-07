from gzip import compress, decompress
from hashlib import sha256
from os.path import join, splitroot
from pickletools import uint8
from turtle import heading
from typing import override
from magnesium.models.references import Ref
from magnesium.models.repository import Repository
from magnesium.models.blob import Blob
from magnesium.models.commit import Commit
from magnesium.models.tree import Tree


class LocalRepository(Repository):
    _basepath: str
    _object_store: str
    _DEFAULT_DATA_ENCODING: str = "utf-8"
    _ASCII_FILE_SEPARATOR: str = "\x1c"
    _ASCII_GROUP_SEPARATOR: str = "\x1d"
    _ASCII_RECORD_SEPARATOR: str = "\x1e"
    _ASCII_UNIT_SEPARATOR: str = "\x1f"

    def __init__(self, path: str) -> None:
        super().__init__()
        self._basepath = path
        self._object_store = join(self._basepath, "objects")
        assert self._DEFAULT_DATA_ENCODING == "utf-8", """
        Se intentó modificar la codificación por defecto de los archivos!

        La codificación debe ser siempre UTF-8.
        """

    def _hash_object(self, data: str) -> str:
        encoded_data = data.encode(self._DEFAULT_DATA_ENCODING)
        sha = sha256(encoded_data).hexdigest()
        return sha

    def _object_path(self, sha: str) -> str:
        final_path = join(self._object_store, sha[:16], sha[16:])
        return final_path

    def _save_object(self, type: str, data: bytes) -> int | None:
        decompressed_content: str = f"{type}{self._ASCII_GROUP_SEPARATOR}{len(data)}{self._ASCII_FILE_SEPARATOR}{data}"
        decompressed_data = decompressed_content.encode(self._DEFAULT_DATA_ENCODING)
        sha = self._hash_object(decompressed_content)
        file = open(self._object_path(sha), "wb")
        compressed_data = compress(decompressed_data)
        return file.write(compressed_data)

    def _load_object(self, sha: str) -> tuple[str, int, bytes] | None:
        file = open(self._object_path(sha), "rb")
        compresseed_data = file.read()
        decompressed_data = decompress(compresseed_data)
        decoded_data = decompressed_data.decode(self._DEFAULT_DATA_ENCODING)
        (header, body) = decoded_data.split(self._ASCII_FILE_SEPARATOR)
        (type, size_str) = header.split(self._ASCII_GROUP_SEPARATOR)

        return (type, int(size_str), body.encode(self._DEFAULT_DATA_ENCODING))

    @override
    def init(self, path: str | None) -> str | None:
        return

    @override
    def save_blob(self, blob: Blob) -> str | None:
        return

    @override
    def load_blob(self, sha: str) -> Blob | None:
        return

    @override
    def save_commit(self, commit: Commit) -> str | None:
        return

    @override
    def load_commit(self, sha: str) -> Commit | None:
        return

    @override
    def save_tree(self, tree: Tree) -> str | None:
        return

    @override
    def load_tree(self, sha: str) -> Tree | None:
        return

    @override
    def save_ref(self, ref: Ref) -> str | None:
        return
