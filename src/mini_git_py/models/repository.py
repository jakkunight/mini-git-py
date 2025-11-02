from mini_git_py.models.git_objects import GitObject
from mini_git_py.models.references import Ref
from gzip import compress, decompress
from os import path, makedirs, getcwd, remove, listdir


class Repository:
    default_head_ref: str = "master"
    content_encoding: str = "utf-8"
    repository_dir: str | None = None
    repository_store: str | None = None
    object_store: str | None = None
    refs_store: str | None = None
    head_store: str | None = None
    head_ref: str = default_head_ref
    refs: list[str] = [default_head_ref]

    def __init__(self):
        pass

    def init(self):
        if self.repository_dir is not None:
            return

        self.repository_dir = getcwd()
        self.repository_store: str = path.join(self.repository_dir, ".mg")
        self.object_store: str = path.join(self.repository_store, "objects")
        self.refs_store: str = path.join(self.repository_store, "refs")
        self.head_store: str = path.join(self.repository_store, "HEAD")

        makedirs(self.repository_store)
        makedirs(self.object_store)
        makedirs(self.refs_store)
        head = open(self.head_store, "xb")
        head.write(self.head_ref.encode(self.content_encoding))
        head.close()

    def store_object(self, object: GitObject):
        object_path: str = path.join(self.object_store, object.sha[0:4], object.sha[4:])
        assert not path.exists(object_path)
        if object.type == "tree":
            # TODO: implement tree content validation
            pass
        elif object.type == "commit":
            # TODO: implement commit content validation
            pass
        elif object.type == "tag":
            # TODO: implement tag content validation
            pass
        else:
            return
        field_separator: str = "\n"
        part_separator: str = "\n\n"
        header: str = f"{object.type}{field_separator}{object.size}"
        object_content: str = f"{header}{part_separator}{object.content}"
        compressed_bytes = compress(object_content.encode(self.content_encoding), 9)
        file = open(
            object_path,
            "wb",
        )

        file.write(compressed_bytes)
        file.close()

    def load_object(self, sha: str) -> GitObject:
        field_separator: str = "\n"
        part_separator: str = "\n\n"
        file = open(
            path.join(self.repository_dir, self.object_store, sha[0:4], sha[4:]), "rb"
        )

        compressed_bytes = file.read()
        decompressed_bytes = decompress(compressed_bytes)
        content_str = decompressed_bytes.decode(self.content_encoding)
        [header, content] = content_str.split(part_separator)
        [type, size] = header.split(field_separator)
        return GitObject(sha, type, int(size), content.encode(self.content_encoding))

    def save_reference(self, ref: Ref):
        ref_path = path.join(self.refs_store, ref.name)
        assert not path.exists(ref_path), f"""
            La referencia ya existe.

            Valor provisto:
            - {ref.name}
        """

        commit_path = path.join(self.object_store, ref.sha[0:4])
        assert not path.exists(commit_path), f"""
            El commit provisto por esta referencia no existe.

            Valor provisto:
            - {ref.sha}
        """

        ref_file = open(ref_path, "xt")
        ref_file.write(ref.sha)

        def update_reference(self, ref: Ref):
            ref_path = path.join(self.refs_store, ref.name)
            assert path.exists(ref_path), f"""
                La referencia no existe.

                Valor provisto:
                - {ref.name}
            """

            commit_path = path.join(self.object_store, ref.sha[0:4])
            assert not path.exists(commit_path), f"""
                El commit provisto por esta referencia no existe.

                Valor provisto:
                - {ref.sha}
            """

            ref_file = open(ref_path, "xt")
            ref_file.write(ref.sha)

        def delete_reference(self, ref_name):
            ref_path: str = path.join(self.refs_store, ref_name)
            assert path.exists(ref_path), f"""
                La referencia no existe.

                Valor provisto:
                - {ref.name}
            """

            remove(ref_path)

        def list_references(self) -> list[Ref] | None:
            references: list[Ref] = []
            for entry in listdir(self.refs_store):
                file = open(path.join(self.refs_store, entry), "rt")
                ref_sha: str = file.read()
                references.append(Ref(entry, ref_sha))

            return references
