# mock_dependencies.py
import gzip
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from re import fullmatch


@dataclass
class Sha256Hash:
    sha: str

    def __post_init__(self):
        try:
            assert fullmatch(r"[0-9a-f]{64}", self.sha), (
                "El formato del hash es inválido. Un hash string sólo puede contener dígitos hexadecimales y debe ser de 256 bits de longitud."
            )
        except Exception as e:
            print(e)


@dataclass
class Blob:
    content: str

    def __post_init__(self):
        pass

    def get_lines(self) -> list[str]:
        return self.content.splitlines(keepends=True)


@dataclass
class Email:
    email: str

    def __post_init__(self):
        try:
            assert fullmatch(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", self.email
            ), "El email ingresado no es válido!"
        except Exception as e:
            print(e)


@dataclass
class DirEntry:
    name: str
    mode: int
    sha: Sha256Hash


@dataclass
class FileEntry:
    name: str
    mode: int
    sha: Sha256Hash


@dataclass
class Tree:
    directories: list[DirEntry]
    files: list[FileEntry]


@dataclass
class Commit:
    author: str
    email: Email
    message: str
    date: datetime
    tree: Sha256Hash
    parents: list[Sha256Hash]

    def __post_init__(self):
        try:
            assert self.author is not None, "El nombre del autor no puede estar vacío."
            assert self.message is not None, "El mensaje provisto no puede estar vacío."
        except Exception as e:
            print(e)


class Utf8Encoder:
    def encode(self, data: str) -> bytes:
        return data.encode("utf-8")

    def decode(self, data: bytes) -> str:
        return data.decode("utf-8")


class GzipCompressor:
    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data)

    def decompress(self, data: bytes) -> bytes:
        return gzip.decompress(data)


class LocalFileStore:
    def write(self, path: Path, data: bytes):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            _ = f.write(data)

    def read(self, path: Path) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def delete(self, path: Path):
        if path.exists():
            path.unlink()


class LocalObjectPathBuilder:
    base_dir: Path

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def build_object_path(self, sha: Sha256Hash) -> Path:
        sha_str = sha.sha
        return self.base_dir / sha_str[:2] / sha_str[2:]

    def exists(self) -> bool:
        return self.base_dir.exists()
