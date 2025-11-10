from hashlib import sha256
from pathlib import Path
from typing import override
from interfaces.repository import (
    BlobRepository,
    CommitRepository,
    IndexRepository,
    ReflogRepository,
    RepositoryHead,
    TreeRepository,
    TagRepository,
    RefRepository,
)
from interfaces.data_compressor import DataCompressor
from interfaces.data_encoder import DataEncoder
from interfaces.file_store import FileStore
from interfaces.serde.blob import BlobSerializer
from interfaces.serde.tree import TreeSerializer
from interfaces.serde.tag import TagSerializer
from interfaces.serde.commit import CommitSerializer
from models.blob import Blob
from models.ref import CommitRef, TagRef
from models.reflog import Reflog
from models.tag import Tag
from models.tree import Tree
from models.commit import Commit
from models.hash import Sha256Hash


class LocalRepository(
    BlobRepository,
    TreeRepository,
    CommitRepository,
    TagRepository,
    RefRepository,
    ReflogRepository,
    RepositoryHead,
    IndexRepository,
):
    _file_store: FileStore
    _blob_serializer: BlobSerializer
    _tree_serializer: TreeSerializer
    _commit_serializer: CommitSerializer
    _tag_serializer: TagSerializer
    _encoder: DataEncoder
    _compressor: DataCompressor
    _base_dir: Path
    _refs_dir: Path
    _reflogs_dir: Path

    def __init__(
        self,
        file_store: FileStore,
        encoder: DataEncoder,
        blob_serializer: BlobSerializer,
        tree_serializer: TreeSerializer,
        commit_serializer: CommitSerializer,
        tag_serializer: TagSerializer,
        compressor: DataCompressor,
        base_dir: Path,
    ) -> None:
        self._file_store = file_store
        self._encoder = encoder
        self._blob_serializer = blob_serializer
        self._tree_serializer = tree_serializer
        self._commit_serializer = commit_serializer
        self._tag_serializer = tag_serializer
        self._compressor = compressor
        self._base_dir = base_dir
        self._refs_dir = base_dir / "refs"
        self._reflogs_dir = self._refs_dir / "logs"

    def _object_path(self, sha: str) -> Path:
        return self._base_dir / "objects" / sha[:2] / sha[2:]

    def _store(self, serialized: str) -> Sha256Hash | None:
        encoded = self._encoder.encode(serialized)
        sha_hex = sha256(encoded).hexdigest()

        try:
            sha_obj = Sha256Hash(sha_hex)
        except Exception:
            return None

        data_to_store = encoded
        compressed = self._compressor.compress(encoded)
        if compressed is None:
            return None
        data_to_store = compressed

        path = self._object_path(sha_hex)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        saved = self._file_store.save(path, data_to_store)
        if saved is None:
            return None

        return sha_obj

    def _load(self, sha: Sha256Hash) -> bytes | None:
        path = self._object_path(sha.sha)
        raw = self._file_store.load(path)
        if raw is None:
            return None

        decompressed = self._compressor.decompress(raw)
        if decompressed is None:
            return None
        encoded = decompressed

        computed = sha256(encoded).hexdigest()
        if computed != sha.sha:
            return None

        return encoded

    # -------------------- BlobRepository --------------------

    @override
    def save_blob(self, blob: Blob) -> Sha256Hash | None:
        serialized = self._blob_serializer.serialize_blob(blob)
        return self._store(serialized)

    @override
    def load_blob(self, sha: Sha256Hash) -> Blob:
        encoded = self._load(sha)
        if encoded is None:
            raise FileNotFoundError(f"No existe blob con SHA: {sha.sha}")

        serialized = self._encoder.decode(encoded)
        return self._blob_serializer.deserialize_blob(serialized)

    # -------------------- TreeRepository --------------------

    @override
    def save_tree(self, tree: Tree) -> Sha256Hash | None:
        serialized = self._tree_serializer.serialize_tree(tree)
        return self._store(serialized)

    @override
    def load_tree(self, sha: Sha256Hash) -> Tree | None:
        encoded = self._load(sha)
        if encoded is None:
            return None

        serialized = self._encoder.decode(encoded)
        return self._tree_serializer.deserialize_tree(serialized)

    # -------------------- CommitRepository --------------------

    @override
    def save_commit(self, commit: Commit) -> str | None:
        serialized = self._commit_serializer.serialize_commit(commit)
        sha_obj = self._store(serialized)
        return sha_obj.sha if sha_obj is not None else None

    @override
    def load_commit(self, sha: Sha256Hash) -> Commit | None:
        encoded = self._load(sha)
        if encoded is None:
            return None

        serialized = self._encoder.decode(encoded)
        return self._commit_serializer.deserialize_commit(serialized)

    # --------------------- TagRepository -----------------------

    @override
    def save_tag(self, tag: Tag) -> Sha256Hash | None:
        serialized = self._tag_serializer.serialize_tag(tag)
        if serialized is None:
            return None
        return self._store(serialized)

    @override
    def load_tag(self, sha: Sha256Hash) -> Tag | None:
        encoded = self._load(sha)
        if encoded is None:
            return None
        serialized = self._encoder.decode(encoded)
        return self._tag_serializer.deserialize_tag(serialized)

    # --------------------- RefRepository -----------------------

    @override
    def save_tag_ref(self, ref: TagRef) -> str | None:
        path = self._refs_dir / "tags" / ref.name
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        saved = self._file_store.save(path, self._encoder.encode(ref.sha.sha))
        if saved is None:
            return None
        return ref.name

    @override
    def load_tag_ref(self, name: str) -> TagRef | None:
        path = self._refs_dir / "tags" / name
        raw = self._file_store.load(path)
        if raw is None:
            return None

        sha_str = self._encoder.decode(raw)
        sha = Sha256Hash(sha_str)
        return TagRef(name, sha)

    @override
    def save_commit_ref(self, ref: CommitRef) -> str | None:
        path = self._refs_dir / "commits" / ref.name
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        saved = self._file_store.save(path, self._encoder.encode(ref.sha.sha))
        if saved is None:
            return None
        return ref.name

    @override
    def load_commit_ref(self, name: str) -> CommitRef | None:
        path = self._refs_dir / "commits" / name
        raw = self._file_store.load(path)
        if raw is None:
            return None

        sha_str = self._encoder.decode(raw)
        sha = Sha256Hash(sha_str)
        return CommitRef(name, sha)

    # ------------------- ReflogRepository ----------------------

    @override
    def load_reflogs(self, ref_name: str) -> Reflog | None:
        path = self._reflogs_dir / ref_name
        raw = self._file_store.load(path)
        if raw is None:
            return None

        text = self._encoder.decode(raw)
        lines = text.strip().split("\n") if text else []
        shas: list[Sha256Hash] = []
        for line in lines:
            try:
                shas.append(Sha256Hash(line))
            except Exception:
                return None

        return Reflog(shas)

    @override
    def save_reflogs(self, ref_name: str) -> Sha256Hash | None:
        path = self._reflogs_dir / ref_name
        raw = self._file_store.load(path)
        if raw is None:
            return None

        sha_hex = sha256(raw).hexdigest()
        try:
            sha_obj = Sha256Hash(sha_hex)
        except Exception:
            return None

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        saved = self._file_store.save(path, raw)
        if saved is None:
            return None

        return sha_obj

    # ------------------- RepositoryHead ----------------------

    @override
    def update_head(self, ref: CommitRef) -> Sha256Hash:
        head_file = self._base_dir / "head"
        _ = head_file.write_text(ref.name + "\n")  # guardamos sólo el nombre de la ref
        return ref.sha

    @override
    def load_head(self) -> CommitRef:
        head_file = self._base_dir / "head"
        if not head_file.exists():
            raise ValueError("El HEAD aún no está definido")
        ref_name = head_file.read_text().strip()
        sha = self.load_commit_ref(ref_name)
        if sha is None:
            raise ValueError(
                f"No se encontró la commit ref '{ref_name}' en el repositorio"
            )
        return sha

    # ------------------- RepositoryIndex ---------------------

    @override
    def save_index(self, index: Tree) -> Sha256Hash | None:
        data_str = self._tree_serializer.serialize_tree(index)
        data_bytes = data_str.encode()
        sha_bytes = sha256(data_bytes).hexdigest()
        sha = Sha256Hash(sha_bytes)
        index_file = self._base_dir / "index"
        _ = index_file.write_bytes(data_bytes)
        return sha

    @override
    def load_index(self) -> Tree | None:
        index_file = self._base_dir / "index"
        if not index_file.exists():
            return None
        data_bytes = index_file.read_bytes()
        data_str = data_bytes.decode()
        return self._tree_serializer.deserialize_tree(data_str)
