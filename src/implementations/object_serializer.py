from typing import override
from datetime import datetime
from interfaces.data_encoder import DataEncoder
from interfaces.serde.blob import BlobSerializer
from interfaces.serde.tag import TagSerializer
from interfaces.serde.tree import TreeSerializer
from interfaces.serde.commit import CommitSerializer
from models import Email, Tag
from models.blob import Blob
from models.hash import Sha256Hash
from models.tree import DirEntry, FileEntry, Tree
from models.commit import Commit


class ObjectSerializer(BlobSerializer, TreeSerializer, CommitSerializer, TagSerializer):
    _encoder: DataEncoder

    def __init__(self, encoder: DataEncoder):
        self._encoder = encoder

    @override
    def serialize_blob(self, blob: Blob) -> str:
        # Codificamos el contenido para medir su tamaño
        content_bytes = self._encoder.encode(blob.content)
        size = len(content_bytes)
        # Cabecera: "tipo\x1Fsize\x00"
        header = f"blob\x1f{size}\x00"
        return header + blob.content

    @override
    def deserialize_blob(self, data: str) -> Blob:
        # Buscamos el separador de cabecera y contenido
        header_end = data.index("\x00")
        header = data[:header_end]
        content = data[header_end + 1 :]
        tipo, size_str = header.split("\x1f")
        if tipo != "blob":
            raise ValueError(f"Tipo inválido en blob: {tipo}")
        # Validamos tamaño
        size = int(size_str)
        if size != len(self._encoder.encode(content)):
            raise ValueError("El tamaño del contenido no coincide con la cabecera")
        return Blob(content=content)

    @override
    def serialize_tree(self, tree: Tree) -> str:
        # Cada entrada se serializa como: tipo\x1Fmode\x1Fname\x1Fsha
        lines: list[str] = []
        for d in tree.directories:
            lines.append(f"dir\x1f{d.mode}\x1f{d.name}\x1f{d.sha.sha}")
        for f in tree.files:
            lines.append(f"file\x1f{f.mode}\x1f{f.name}\x1f{f.sha.sha}")
        content_str = "\n".join(lines)
        content_bytes = self._encoder.encode(content_str)
        header = f"tree\x1f{len(content_bytes)}\x00"
        return header + content_str

    @override
    def deserialize_tree(self, data: str) -> Tree:
        header_end = data.index("\x00")
        header = data[:header_end]
        content = data[header_end + 1 :]
        tipo, size_str = header.split("\x1f")
        if tipo != "tree":
            raise ValueError(f"Tipo inválido en tree: {tipo}")
        size = int(size_str)
        if size != len(self._encoder.encode(content)):
            raise ValueError("El tamaño del contenido no coincide con la cabecera")

        directories: list[DirEntry] = []
        files: list[FileEntry] = []
        for line in content.split("\n"):
            entry_type, mode_str, name, sha_str = line.split("\x1f")
            mode = int(mode_str)
            sha = Sha256Hash(sha_str)
            if entry_type == "dir":
                directories.append(DirEntry(name=name, mode=mode, sha=sha))
            elif entry_type == "file":
                files.append(FileEntry(name=name, mode=mode, sha=sha))
            else:
                raise ValueError(f"Tipo de entrada inválido: {entry_type}")
        return Tree(directories=directories, files=files)

    @override
    def serialize_commit(self, commit: Commit) -> str:
        parents_str = ",".join(p.sha for p in commit.parents)
        content_lines = [
            f"author\x1f{commit.author}",
            f"email\x1f{commit.email.email}",
            f"date\x1f{int(commit.date.timestamp())}",  # guardamos como timestamp
            f"tree\x1f{commit.tree.sha}",
            f"parents\x1f{parents_str}",
            f"message\x1f{commit.message}",
        ]
        content_str = "\n".join(content_lines)
        content_bytes = self._encoder.encode(content_str)
        header = f"commit\x1f{len(content_bytes)}\x00"
        return header + content_str

    @override
    def deserialize_commit(self, data: str) -> Commit:
        header_end = data.index("\x00")
        header = data[:header_end]
        content = data[header_end + 1 :]
        tipo, size_str = header.split("\x1f")
        if tipo != "commit":
            raise ValueError(f"Tipo inválido en commit: {tipo}")
        size = int(size_str)
        if size != len(self._encoder.encode(content)):
            raise ValueError("El tamaño del contenido no coincide con la cabecera")

        fields: dict[str, str] = {}
        for line in content.split("\n"):
            key, value = line.split("\x1f", 1)
            fields[key] = value

        author = fields["author"]
        email = Email(fields["email"])
        date = datetime.fromtimestamp(int(fields["date"]))
        tree = Sha256Hash(fields["tree"])
        parents = [Sha256Hash(p) for p in fields["parents"].split(",") if p]

        return Commit(
            author=author,
            email=email,
            date=date,
            tree=tree,
            parents=parents,
            message=fields["message"],
        )

    @override
    def serialize_tag(self, tag: Tag) -> str | None:
        content_lines = [
            f"title\x1f{tag.title}",
            f"body\x1f{tag.body}",
            f"commit\x1f{tag.commit.sha}",
            f"author\x1f{tag.author}",
            f"email\x1f{tag.email.email}",
            f"date\x1f{int(tag.date.timestamp())}",
        ]
        content_str = "\n".join(content_lines)
        content_bytes = self._encoder.encode(content_str)
        header = f"tag\x1f{len(content_bytes)}\x00"
        return header + content_str

    @override
    def deserialize_tag(self, data: str) -> Tag | None:
        if not data:
            return None
        header_end = data.index("\x00")
        header = data[:header_end]
        content = data[header_end + 1 :]
        tipo, size_str = header.split("\x1f")
        if tipo != "tag":
            raise ValueError(f"Tipo inválido en tag: {tipo}")
        size = int(size_str)
        if size != len(self._encoder.encode(content)):
            raise ValueError("El tamaño del contenido no coincide con la cabecera")

        fields: dict[str, str] = {}
        for line in content.split("\n"):
            key, value = line.split("\x1f", 1)
            fields[key] = value

        return Tag(
            title=fields["title"],
            body=fields["body"],
            commit=Sha256Hash(fields["commit"]),
            author=fields["author"],
            email=Email(fields["email"]),
            date=datetime.fromtimestamp(int(fields["date"])),
        )
