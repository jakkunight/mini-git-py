from gzip import compress, decompress
from hashlib import sha256
from os import getcwd, makedirs
from os.path import exists, join
from re import match
from typing import override
from os import listdir, remove
from magnesium.models.references import Ref
from magnesium.models.repository import Repository
from magnesium.models.blob import Blob
from magnesium.models.commit import Commit
from magnesium.models.tag import Tag
from magnesium.models.tree import Tree, TreeEntry, BlobEntry


class LocalRepository(Repository):
    _basepath: str
    _object_store: str
    _refs_store: str
    _index: str
    _head: str
    _DEFAULT_DATA_ENCODING: str = "utf-8"
    _ASCII_FILE_SEPARATOR: str = "\x1c"
    _ASCII_GROUP_SEPARATOR: str = "\x1d"
    _ASCII_RECORD_SEPARATOR: str = "\x1e"
    _ASCII_UNIT_SEPARATOR: str = "\x1f"
    _DEFAULT_HASH_PATH_STRIP: int = 16
    _FIRST_COMMIT_PARENT_HASH: str = "0" * 40

    def __init__(self) -> None:
        super().__init__()

    def _save_object(self, type: str, body: str) -> str | None:
        """
        Un helper para escribir un objeto en disco y almacenarlo.
        Devuelve el SHA-256 del objeto guardado.

        Si la operación falla, se devuelve un `None` como resultado (nil-as-error)
        """
        header: str = f"{type}{self._ASCII_RECORD_SEPARATOR}{len(body.encode(self._DEFAULT_DATA_ENCODING))}"
        content: str = f"{header}{self._ASCII_UNIT_SEPARATOR}{body}"
        encoded_content: bytes = content.encode(self._DEFAULT_DATA_ENCODING)
        sha: str = sha256(encoded_content).hexdigest()
        compressed_content: bytes = compress(encoded_content)
        try:
            filepath = join(
                self._object_store,
                sha[: self._DEFAULT_HASH_PATH_STRIP],
                sha[self._DEFAULT_HASH_PATH_STRIP :],
            )
            if exists(filepath):
                return sha
            dirpath = join(
                self._object_store,
                sha[: self._DEFAULT_HASH_PATH_STRIP],
            )
            makedirs(dirpath)
            file = open(
                filepath,
                "wb",
            )
            _ = file.write(compressed_content)
            file.close()
        except Exception as e:
            print(e)
            return None

        return sha

    def _load_object(self, sha: str) -> tuple[str, str] | None:
        """
        Un helper para leer un objeto del disco y devolverlo para su decodificación.
        """
        try:
            assert match(r"^[a-f0-9]{64}$", sha), """
            El SHA-256 es inválido.
            """
            file = open(
                join(
                    self._object_store,
                    sha[: self._DEFAULT_HASH_PATH_STRIP],
                    sha[self._DEFAULT_HASH_PATH_STRIP :],
                ),
                "rb",
            )
            compressed_content: bytes = file.read()
            encoded_content: bytes = decompress(compressed_content)
            assert sha == sha256(encoded_content), """
            El archivo se corrompió!
            """
            content: str = encoded_content.decode(self._DEFAULT_DATA_ENCODING)
            (header, body) = content.split(self._ASCII_UNIT_SEPARATOR)
            (type, size_str) = header.split(self._ASCII_RECORD_SEPARATOR)
            assert int(size_str) == len(body), """
            El archivo se corrompió!
            """
        except Exception:
            return None
        return (type, body)

    @override
    def init(self, path: str | None) -> str | None:
        if path is None:
            path = getcwd()
        self._basepath = join(path, ".mg")
        self._object_store = join(self._basepath, "objects")
        self._refs_store = join(self._basepath, "refs")
        self._index = join(self._basepath, "index")
        self._head = join(self._basepath, "head")
        assert self._DEFAULT_DATA_ENCODING == "utf-8", """
        Se intentó modificar la codificación por defecto de los archivos!

        La codificación debe ser siempre UTF-8.
        """
        if exists(self._basepath):
            return path
        try:
            makedirs(self._basepath)
            makedirs(self._object_store)
            makedirs(self._refs_store)
            index = open(self._index, "xb")
            _ = index.write(b"")
            index.close()
            head = open(self._head, "xb")
            _ = head.write(b"")
            head.close()
        except Exception:
            return None
        return path

    @override
    def save_blob(self, blob: Blob) -> str | None:
        return self._save_object(blob.type, blob.content)

    @override
    def load_blob(self, sha: str) -> Blob | None:
        result = self._load_object(sha)
        if result is None:
            return None
        (type, content) = result
        blob = Blob(content, type)
        return blob

    @override
    def save_commit(self, commit: Commit) -> str | None:
        body: str = f"{commit.author}{self._ASCII_RECORD_SEPARATOR}"
        body += f"{commit.email}{self._ASCII_RECORD_SEPARATOR}"
        body += f"{commit.date}{self._ASCII_RECORD_SEPARATOR}"
        body += f"{commit.message}{self._ASCII_RECORD_SEPARATOR}"
        if not exists(
            join(
                self._object_store,
                commit.tree[: self._DEFAULT_HASH_PATH_STRIP],
                commit.tree[self._DEFAULT_HASH_PATH_STRIP :],
            )
        ):
            return None
        body += f"{commit.tree}"
        for parent in commit.parents:
            # Si no nay un commit padre, entonces se omite.
            if parent != "":
                continue
            # Si el commit padre no existe, se retorna con error.
            if not exists(
                join(
                    self._object_store,
                    parent[: self._DEFAULT_HASH_PATH_STRIP],
                    parent[self._DEFAULT_HASH_PATH_STRIP :],
                )
            ):
                return None
            body += f"{parent}{self._ASCII_RECORD_SEPARATOR}"

        return self._save_object(commit.type, body)

    @override
    def save_tree(self, tree: Tree) -> str | None:
        lines: list[str] = []
        for entry in tree.tree_entries:
            lines.append(
                f"tree{self._ASCII_RECORD_SEPARATOR}{entry.mode}{self._ASCII_RECORD_SEPARATOR}{entry.name}{self._ASCII_RECORD_SEPARATOR}{entry.sha}"
            )
        for entry in tree.blob_entries:
            lines.append(
                f"blob{self._ASCII_RECORD_SEPARATOR}{entry.mode}{self._ASCII_RECORD_SEPARATOR}{entry.name}{self._ASCII_RECORD_SEPARATOR}{entry.sha}"
            )
        body = self._ASCII_UNIT_SEPARATOR.join(lines)
        return self._save_object(tree.type, body)

    @override
    def load_tree(self, sha: str) -> Tree | None:
        result = self._load_object(sha)
        if result is None:
            return None
        (_, content) = result
        tree_entries: list[TreeEntry] = []
        blob_entries: list[BlobEntry] = []
        for line in content.split(self._ASCII_UNIT_SEPARATOR):
            t, mode, name, s = line.split(self._ASCII_RECORD_SEPARATOR)
            mode = int(mode)
            if t == "tree":
                tree_entries.append(TreeEntry(mode, name, s))
            else:
                blob_entries.append(BlobEntry(mode, name, s))
        return Tree(tree_entries, blob_entries)

    @override
    def save_ref(self, ref: Ref) -> str | None:
        try:
            with open(
                join(self._refs_store, ref.name),
                "wt",
                encoding=self._DEFAULT_DATA_ENCODING,
            ) as f:
                _ = f.write(f"{ref.type}{self._ASCII_RECORD_SEPARATOR}{ref.sha}")
        except Exception:
            return None
        return ref.sha

    @override
    def load_ref(self, name: str) -> Ref | None:
        path = join(self._refs_store, name)
        if not exists(path):
            return None
        try:
            with open(path, "r", encoding=self._DEFAULT_DATA_ENCODING) as f:
                content = f.read()
            t, sha = content.split(self._ASCII_RECORD_SEPARATOR)
            return Ref(name, sha, t)
        except Exception:
            return None

    @override
    def list_refs(self) -> list[Ref] | None:
        try:
            refs: list[Ref] = []
            for name in listdir(self._refs_store):
                r = self.load_ref(name)
                if r is not None:
                    refs.append(r)
            return refs
        except Exception:
            return None

    @override
    def update_ref(self, ref: Ref) -> str | None:
        old = self.load_ref(ref.name)
        old_sha = old.sha if old else None
        result = self.save_ref(ref)
        return old_sha if result else None

    @override
    def delete_ref(self, name: str) -> str | None:
        old = self.load_ref(name)
        if old is None:
            return None
        try:
            remove(join(self._refs_store, name))
        except Exception:
            return None
        return old.sha

    @override
    def save_tag(self, tag: Tag) -> str | None:
        body = f"{tag.name}{self._ASCII_RECORD_SEPARATOR}{tag.message}{self._ASCII_RECORD_SEPARATOR}{tag.commit}"
        sha = self._save_object(tag.type, body)
        if sha is None:
            return None
        # Creamos una ref de tipo tag
        result = self.save_ref(Ref(tag.name, sha, "tag"))
        if result is None:
            return None
        return sha

    @override
    def load_tag(self, name: str) -> Tag | None:
        ref = self.load_ref(name)
        if ref is None or ref.type != "tag":
            return None
        obj = self._load_object(ref.sha)
        if obj is None:
            return None
        (_, body) = obj
        tag_name, msg, commit = body.split(self._ASCII_RECORD_SEPARATOR)
        return Tag(tag_name, msg, commit)

    @override
    def load_commit(self, sha: str) -> Commit | None:
        result = self._load_object(sha)
        if result is None:
            return None
        (_, body) = result
        parts = body.split(self._ASCII_RECORD_SEPARATOR)
        author, email, date, message, tree_and_parents = (
            parts[0],
            parts[1],
            parts[2],
            parts[3],
            parts[4:],
        )
        tree = tree_and_parents[0]
        parents = tree_and_parents[1:] if len(tree_and_parents) > 1 else []
        return Commit(author, email, message, date, parents, tree)

    @override
    def log_ref(self, name: str) -> list[Commit] | None:
        ref = self.load_ref(name)
        if ref is None:
            return None
        commits: list[Commit] = []
        current = ref.sha
        while current != self._FIRST_COMMIT_PARENT_HASH:
            c = self.load_commit(current)
            if c is None:
                break
            commits.append(c)
            if len(c.parents) == 0:
                break
            current = c.parents[0]
        return commits

    @override
    def log_refs(self) -> list[Commit] | None:
        seen: set[str] = set()
        out: list[Commit] = []
        refs = self.list_refs()
        if refs is None:
            return None
        for r in refs:
            result = self.log_ref(r.name)
            if result is None:
                return None
            commits: list[Commit] = result
            for c in commits:
                if c.tree not in seen:
                    seen.add(c.tree)
                    out.append(c)

        return out

    @override
    def update_head_ref(self, ref: Ref) -> str | None:
        return self.save_ref(ref)

    @override
    def update_index(self, working_tree: Tree) -> str | None:
        sha = self.save_tree(working_tree)
        if sha is None:
            return None
        with open(self._index, "w", encoding=self._DEFAULT_DATA_ENCODING) as f:
            _ = f.write(sha)
        return sha

    @override
    def load_index(self) -> Tree | None:
        if not exists(self._index):
            return None
        with open(self._index, "r", encoding=self._DEFAULT_DATA_ENCODING) as f:
            sha = f.read().strip()
        return self.load_tree(sha)
