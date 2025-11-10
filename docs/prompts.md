Toma en cuenta los siguientes modelos de datos:

```python
from dataclasses import dataclass
from re import fullmatch


@dataclass
class Blob:
    content: str

    def __post_init__(self):
        pass


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


@dataclass
class Tag:
    title: str
    body: str
    commit: Sha256Hash
    author: str
    email: Email
    date: datetime

    def __post_init__(self):
        try:
            assert self.author is not None, "El nombre del autor no puede estar vacío."
            assert self.title is not None, (
                "El título del tag provisto no puede estar vacío."
            )
            assert self.body is not None, "El mensaje provisto no puede estar vacío."
        except Exception as e:
            print(e)


@dataclass
class CommitRef:
    name: str
    sha: Sha256Hash

    def __post_init__(self):
        try:
            assert self.name is not None, (
                "El nombre de la referencia no puede estar vacío."
            )
        except Exception as e:
            print(e)


@dataclass
class TagRef:
    name: str
    sha: Sha256Hash

    def __post_init__(self):
        try:
            assert self.name is not None, (
                "El nombre de la referencia no puede estar vacío."
            )
        except Exception as e:
            print(e)


@dataclass
class Reflog:
    log: list[Sha256Hash]

    def __post_init__(self):
        pass
```

Y las siguientes interfaces:

```python
from abc import ABC, abstractmethod
from pathlib import Path


class FileStore(ABC):
    @abstractmethod
    def save(self, path: Path, data: bytes) -> int | None:
        pass

    @abstractmethod
    def load(self, path: Path) -> bytes | None:
        pass

class DataEncoder(ABC):
    @abstractmethod
    def encode(self, data: str) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> str:
        pass

class DataCompressor(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes | None:
        pass

    @abstractmethod
    def decompress(self, data: bytes) -> bytes | None:
        pass

class BlobSerializer(ABC):
    @abstractmethod
    def serialize_blob(self, blob: Blob) -> str:
        pass

    @abstractmethod
    def deserialize_blob(self, data: str) -> Blob:
        pass

class TreeSerializer(ABC):
    @abstractmethod
    def serialize_tree(self, tree: Tree) -> str:
        pass

    @abstractmethod
    def deserialize_tree(self, data: str) -> Tree:
        pass

class CommitSerializer(ABC):
    @abstractmethod
    def serialize_commit(self, commit: Commit) -> str:
        pass

    @abstractmethod
    def deserialize_commit(self, data: str) -> Commit:
        pass

class TagSerializer(ABC):
    @abstractmethod
    def serialize_tag(self, tag: Tag) -> str | None:
        pass

    @abstractmethod
    def deserialize_tag(self, data: str) -> Tag | None:
        pass
```

Crea una clase que implemente la siguiente interfaz:

```python
class BlobRepository(ABC):
    @abstractmethod
    def save_blob(self, blob: Blob) -> Sha256Hash | None:
        pass

    @abstractmethod
    def load_blob(self, sha: Sha256Hash) -> Blob:
        pass
```
