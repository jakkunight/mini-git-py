from mini_git_py.models.commit import Commit
from mini_git_py.models.blob import Blob
from mini_git_py.models.tree import Tree
from mini_git_py.models.tag import Tag
from mini_git_py.models.references import Ref
from gzip import compress, decompress
from os import makedirs, getcwd, remove, listdir
from os.path import join, exists
from hashlib import sha256


class LocalRepository:
    _default_head_ref: str = "master"
    _content_encoding: str = "utf-8"
    _repository_dir: str | None = None
    _repository_store: str | None = None
    _object_store: str | None = None
    _refs_store: str | None = None
    _head_store: str | None = None
    _head_ref: str = _default_head_ref
    _refs: list[str] = [_default_head_ref]
    _index_store: str | None

    # INFO: Delimitadores ASCII
    # Se usan los delimitadores ASCII estándar para delimitar información guardada en el repositorio.
    _record_separator: str = "\x1e"
    _unit_separator: str = "\x1f"
    _group_separator: str = "\x1d"

    def __init__(self):
        pass

    def init(self):
        if self._repository_dir is not None:
            return

        self._repository_dir = getcwd()
        self._repository_store: str = join(self._repository_dir, ".mg")
        self._object_store: str = join(self._repository_store, "objects")
        self._refs_store: str = join(self._repository_store, "refs")
        self._head_store: str = join(self._repository_store, "HEAD")
        self._index_store: str = join(self._repository_store, "index")

        makedirs(self._repository_store)
        makedirs(self._object_store)
        makedirs(self._refs_store)
        head = open(self._head_store, "xb")
        head.write(self._head_ref.encode(self._content_encoding))
        head.close()

    def save_commit(self, commit: Commit) -> str | None:
        field_separator: str = "\t"
        separator: str = "\n\n"
        body: str = f"tree {commit.tree}{field_separator}"
        for parent in commit.parents:
            body += f"parent {parent}{field_separator}"

        body += f"date {commit.date}{field_separator}"
        body += f"author {commit.author}{field_separator}"
        body += f"email {commit.email}{field_separator}"
        body += f"message {commit.message}"

        header: str = f"type {commit.type}{field_separator}size {len(body.encode(self._content_encoding))}"
        buffer: str = f"{header}{separator}{body}"
        sha: str = sha256(buffer.encode(self._content_encoding)).hexdigest()
        object_path: str = join(self._object_store, sha[0:4], sha[4:])

        compressed_bytes = compress(buffer.encode(self._content_encoding), 9)
        file = open(
            object_path,
            "wb",
        )

        file.write(compressed_bytes)
        file.close()

        return sha

    def save_tree(self, tree: Tree) -> str | None:
        field_separator: str = "\t"
        separator: str = "\n\n"
        entry_separator: str = "\n"
        body: str = ""
        for entry in tree.entries:
            body += f"mode {entry.mode}{field_separator}"
            body += f"name {entry.name}{field_separator}"
            body += f"sha {entry.sha}{entry_separator}"

        header: str = f"type {tree.type}{field_separator}size {len(body.encode(self._content_encoding))}"
        buffer: str = f"{header}{separator}{body}"
        sha: str = sha256(buffer.encode(self._content_encoding)).hexdigest()
        object_path: str = join(self._object_store, sha[0:4], sha[4:])

        compressed_bytes = compress(buffer.encode(self._content_encoding), 9)
        file = open(
            object_path,
            "wb",
        )

        file.write(compressed_bytes)
        file.close()

        return sha

    def save_blob(self, blob: Blob) -> str | None:
        field_separator: str = "\t"
        separator: str = "\n\n"
        body: bytes = blob.content
        header: str = f"type {blob.type}{field_separator}size{len(body)}"
        buffer: str = f"{header}{separator}{body}"
        sha: str = sha256(buffer.encode(self._content_encoding)).hexdigest()
        object_path: str = join(self._object_store, sha[0:4], sha[4:])

        compressed_bytes = compress(buffer.encode(self._content_encoding), 9)
        file = open(
            object_path,
            "wb",
        )

        file.write(compressed_bytes)
        file.close()

        return sha

    def save_tag(self, tag: Tag) -> str | None:
        field_separator: str = "\t"
        separator: str = "\n\n"
        body: str = f"name {tag.name}{field_separator}commit {tag.commit}"
        header: str = f"type {tag.type}{field_separator}size {len(body.encode(self._content_encoding))}"
        buffer: str = f"{header}{separator}{body}"
        sha: str = sha256(buffer.encode(self._content_encoding)).hexdigest()
        object_path: str = join(self._object_store, sha[0:4], sha[4:])

        compressed_bytes = compress(buffer.encode(self._content_encoding), 9)
        file = open(
            object_path,
            "wb",
        )

        file.write(compressed_bytes)
        file.close()

        return sha

    def load_commit(self, sha: str) -> Commit | None:
        field_separator: str = "\t"
        separator: str = "\n\n"
        file = open(
            join(self._repository_dir, self._object_store, sha[0:4], sha[4:]), "rb"
        )

        compressed_bytes = file.read()
        decompressed_bytes = decompress(compressed_bytes)
        content_str = decompressed_bytes.decode(self._content_encoding)
        [header, body] = content_str.split(separator)
        [type, size] = header.split(field_separator)

        [label, value] = type.split(" ")
        if label == "type" and value != "commit":
            return None

        tree: str = ""
        parents: list[str] = []
        author: str = ""
        email: str = ""
        date: str = ""
        message: str = ""
        for field in body.split(field_separator):
            [label, value] = field.split(" ")
            if label == "tree":
                continue
            elif label == "parent":
                continue
            elif label == "author":
                continue
            elif label == "email":
                continue
            elif label == "date":
                continue
            elif label == "message":
                continue
            else:
                continue

        pass

    def load_tree(self, sha: str) -> Tree | None:
        #     field_separator: str = "\n"
        #     separator: str = "\n\n"
        #     file = open(
        #         join(self.repository_dir, self.object_store, sha[0:4], sha[4:]), "rb"
        #     )

        #     compressed_bytes = file.read()
        #     decompressed_bytes = decompress(compressed_bytes)
        #     content_str = decompressed_bytes.decode(self.content_encoding)
        #     [header, content] = content_str.split(separator)
        #     [type, size] = header.split(field_separator)
        pass

    def load_blob(self, sha: str) -> Blob | None:
        #     field_separator: str = "\n"
        #     separator: str = "\n\n"
        #     file = open(
        #         join(self.repository_dir, self.object_store, sha[0:4], sha[4:]), "rb"
        #     )

        #     compressed_bytes = file.read()
        #     decompressed_bytes = decompress(compressed_bytes)
        #     content_str = decompressed_bytes.decode(self.content_encoding)
        #     [header, content] = content_str.split(separator)
        #     [type, size] = header.split(field_separator)
        pass

    def load_tag(self, sha: str) -> Tag | None:
        #     field_separator: str = "\n"
        #     separator: str = "\n\n"
        #     file = open(
        #         join(self.repository_dir, self.object_store, sha[0:4], sha[4:]), "rb"
        #     )

        #     compressed_bytes = file.read()
        #     decompressed_bytes = decompress(compressed_bytes)
        #     content_str = decompressed_bytes.decode(self.content_encoding)
        #     [header, content] = content_str.split(separator)
        #     [type, size] = header.split(field_separator)
        pass

    # def store_object(self, object: GitObject):
    #     object_path: str = join(self.object_store, object.sha[0:4], object.sha[4:])
    #     assert not exists(object_path)
    #     if object.type == "tree":
    #         # TODO: implement tree content validation
    #         pass
    #     elif object.type == "commit":
    #         # TODO: implement commit content validation
    #         pass
    #     elif object.type == "tag":
    #         # TODO: implement tag content validation
    #         pass
    #     else:
    #         return
    #     field_separator: str = "\n"
    #     part_separator: str = "\n\n"
    #     header: str = f"{object.type}{field_separator}{object.size}"
    #     object_content: str = f"{header}{part_separator}{object.content}"
    #     compressed_bytes = compress(object_content.encode(self.content_encoding), 9)
    #     file = open(
    #         object_path,
    #         "wb",
    #     )

    #     file.write(compressed_bytes)
    #     file.close()

    # def load_object(self, sha: str) -> GitObject:
    #     field_separator: str = "\n"
    #     part_separator: str = "\n\n"
    #     file = open(
    #         join(self.repository_dir, self.object_store, sha[0:4], sha[4:]), "rb"
    #     )

    #     compressed_bytes = file.read()
    #     decompressed_bytes = decompress(compressed_bytes)
    #     content_str = decompressed_bytes.decode(self.content_encoding)
    #     [header, content] = content_str.split(part_separator)
    #     [type, size] = header.split(field_separator)
    #     return GitObject(sha, type, int(size), content.encode(self.content_encoding))

    def save_reference(self, ref: Ref):
        ref_path = join(self._refs_store, ref.name)
        assert not exists(ref_path), f"""
            La referencia ya existe.

            Valor provisto:
            - {ref.name}
        """

        commit_path = join(self._object_store, ref.sha[0:4])
        assert not exists(commit_path), f"""
            El commit provisto por esta referencia no existe.

            Valor provisto:
            - {ref.sha}
        """

        ref_file = open(ref_path, "xt")
        ref_file.write(ref.sha)

    def update_reference(self, ref: Ref):
        ref_path = join(self._refs_store, ref.name)
        assert exists(ref_path), f"""
            La referencia no existe.

            Valor provisto:
            - {ref.name}
        """

        commit_path = join(self._object_store, ref.sha[0:4])
        assert not exists(commit_path), f"""
            El commit provisto por esta referencia no existe.

            Valor provisto:
            - {ref.sha}
        """

        ref_file = open(ref_path, "xt")
        ref_file.write(ref.sha)

    def delete_reference(self, ref_name):
        ref_path: str = join(self._refs_store, ref_name)
        assert exists(ref_path), f"""
            La referencia no existe.

            Valor provisto:
            - {ref_name}
        """

        remove(ref_path)

    def list_references(self) -> list[Ref] | None:
        references: list[Ref] = []
        ref_store = listdir(self._refs_store)
        if len(ref_store) == 0:
            return None

        for entry in ref_store:
            file = open(join(self._refs_store, entry), "rt")
            ref_sha: str = file.read()
            references.append(Ref(entry, ref_sha))

        return references

    def update_head(self, ref: Ref):
        ref_path: str = join(self._refs_store, ref.name)
        head = open(self._head_store, "wt")
        head.write(ref.name)
        assert exists(ref_path), f"""
            La referencia no existe.

            Valor provisto:
            - {ref.name}
        """
