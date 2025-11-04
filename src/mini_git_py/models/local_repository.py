# WARN:
# Este código ha sido generado 100% con IA (GPT-5 free).
# El proceso de elaboración corresponde a la implementación de la interfaz
# `Repository`, que fue creada por @Santiago Wu. También se sumistraron como
# entrada del prompt los tipos de datos `Commit`, `Blob`, `Tree`, `Ref`, `Tag`
# y `TreeEntry`, lo que garantiza la consistencia y contexto suficientes para
# la implementación.
#
# El código ha sido íntegramente analizado por @Santiago Wu.

import os
import gzip
import hashlib
import shutil
from typing import List, Optional, Tuple
from mini_git_py.models.repository import Repository
from mini_git_py.models.commit import Commit
from mini_git_py.models.blob import Blob
from mini_git_py.models.tree import Tree, TreeEntry
from mini_git_py.models.tag import Tag
from mini_git_py.models.references import Ref

FIELD_SEP = chr(0x1C)
SECTION_SEP = chr(0x1D)


class LocalRepository(Repository):
    work_path: str
    repo_path: str
    objects_path: str
    refs_path: str
    head_path: str
    index_path: str

    def __init__(self, path: Optional[str] = None) -> None:
        self.work_path = os.path.abspath(path or os.getcwd())
        self.repo_path = os.path.join(self.work_path, ".mg")
        self.objects_path = os.path.join(self.repo_path, "objects")
        self.refs_path = os.path.join(self.repo_path, "refs")
        self.head_path = os.path.join(self.repo_path, "HEAD")
        self.index_path = os.path.join(self.repo_path, "index")

    # --------------------------
    # Init repo
    # --------------------------
    def init(self, path: Optional[str] = None) -> Optional[str]:
        self.work_path = os.path.abspath(path or os.getcwd())
        self.repo_path = os.path.join(self.work_path, ".mg")
        self.objects_path = os.path.join(self.repo_path, "objects")
        self.refs_path = os.path.join(self.repo_path, "refs")
        self.head_path = os.path.join(self.repo_path, "HEAD")
        self.index_path = os.path.join(self.repo_path, "index")

        try:
            os.makedirs(self.repo_path, exist_ok=True)
            os.makedirs(self.objects_path, exist_ok=True)
            os.makedirs(self.refs_path, exist_ok=True)
            if not os.path.exists(self.head_path):
                with open(self.head_path, "w") as f:
                    f.write("ref: refs/main")
            return self.repo_path
        except Exception:
            return None

    # --------------------------
    # Formato estilo Git + gzip
    # --------------------------
    def _encode(self, obj_type: str, body: bytes) -> bytes:
        header: str = f"{obj_type}{FIELD_SEP}{len(body)}"
        raw: bytes = header.encode() + SECTION_SEP.encode() + body
        return gzip.compress(raw)

    def _decode(self, compressed: bytes) -> Tuple[str, bytes]:
        raw: bytes = gzip.decompress(compressed)
        header, body = raw.split(SECTION_SEP.encode(), 1)
        obj_type, _size = header.decode().split(FIELD_SEP)
        return obj_type, body

    def _save_raw(self, obj_type: str, body: bytes) -> str:
        data: bytes = self._encode(obj_type, body)
        sha: str = hashlib.sha256(data).hexdigest()
        prefix, suffix = sha[:4], sha[4:]
        dirpath: str = os.path.join(self.objects_path, prefix)
        os.makedirs(dirpath, exist_ok=True)
        filepath: str = os.path.join(dirpath, suffix)
        with open(filepath, "wb") as f:
            f.write(data)
        return sha

    def _load_raw(self, sha: str) -> Optional[Tuple[str, bytes]]:
        prefix, suffix = sha[:4], sha[4:]
        filepath: str = os.path.join(self.objects_path, prefix, suffix)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "rb") as f:
            compressed: bytes = f.read()
        return self._decode(compressed)

    def load_object(self, sha: str) -> Optional[Tuple[str, bytes]]:
        return self._load_raw(sha)

    # --------------------------
    # BLOBS
    # --------------------------
    def save_blob(self, blob: Blob) -> Optional[str]:
        try:
            header: bytes = f"{blob.mode}\n{blob.name}\n".encode()
            body: bytes = header + blob.content
            return self._save_raw("blob", body)
        except Exception:
            return None

    def load_blob(self, sha: str) -> Optional[Blob]:
        out = self._load_raw(sha)
        if not out:
            return None
        _, body = out
        mode, name, content = body.split(b"\n", 2)
        return Blob(name=name.decode(), mode=int(mode.decode()), content=content)

    # --------------------------
    # TREES
    # --------------------------
    def save_tree(self, tree: Tree) -> Optional[str]:
        try:
            lines: List[str] = [f"name {tree.name}"]
            for e in tree.entries:
                lines.append(f"{e.mode} {e.name} {e.sha} {e.obj_type}")
            body: bytes = "\n".join(lines).encode()
            return self._save_raw("tree", body)
        except Exception:
            return None

    def load_tree(self, sha: str) -> Optional[Tree]:
        out = self._load_raw(sha)
        if not out:
            return None
        _, body = out
        lines: List[str] = body.decode().splitlines()
        tree_name: str = lines[0].split(" ", 1)[1]
        entries: List[TreeEntry] = []
        for line in lines[1:]:
            mode, name, entry_sha, obj_type = line.split(" ", 3)
            entries.append(TreeEntry(int(mode), name, entry_sha, obj_type))
        return Tree(name=tree_name, entries=entries)

    # --------------------------
    # COMMITS
    # --------------------------
    def save_commit(self, commit: Commit) -> Optional[str]:
        try:
            parts: List[str] = [f"tree {commit.tree}"]
            for p in commit.parents:
                if p:
                    parts.append(f"parent {p}")
            parts.append(f"author {commit.author} <{commit.email}>")
            parts.append(f"date {commit.date}")
            parts.append("message")
            parts.append(commit.message)
            body: bytes = "\n".join(parts).encode()
            return self._save_raw("commit", body)
        except Exception:
            return None

    def load_commit(self, sha: str) -> Optional[Commit]:
        out = self._load_raw(sha)
        if not out:
            return None
        _, body = out
        lines: List[str] = body.decode().split("\n")
        msg_index: int = lines.index("message")
        message: str = "\n".join(lines[msg_index + 1 :])
        tree: str = ""
        parents: List[str] = []
        author: str = ""
        email: str = ""
        date: str = ""
        for line in lines[:msg_index]:
            if line.startswith("tree "):
                tree = line.split(" ", 1)[1]
            elif line.startswith("parent "):
                parents.append(line.split(" ", 1)[1])
            elif line.startswith("author "):
                a = line[len("author ") :]
                author, mail = a.rsplit(" ", 1)
                email = mail.strip("<>")
            elif line.startswith("date "):
                date = line.split(" ", 1)[1]
        return Commit(
            author=author,
            email=email,
            message=message,
            date=date,
            parents=parents,
            tree=tree,
        )

    # --------------------------
    # TAGS
    # --------------------------
    def save_tag(self, tag: Tag) -> Optional[str]:
        try:
            body: bytes = f"tag {tag.name}\nref {tag.commit}\n".encode()
            return self._save_raw("tag", body)
        except Exception:
            return None

    def load_tag(self, sha: str) -> Optional[Tag]:
        out = self._load_raw(sha)
        if not out:
            return None
        _, body = out
        name: str = ""
        commit: str = ""
        for line in body.decode().splitlines():
            if line.startswith("tag "):
                name = line.split(" ", 1)[1]
            elif line.startswith("ref "):
                commit = line.split(" ", 1)[1]
        return Tag(name=name, commit=commit)

    # --------------------------
    # REFERENCIAS
    # --------------------------
    def save_ref(self, ref: Ref) -> Optional[str]:
        try:
            filepath: str = os.path.join(self.refs_path, ref.name)
            with open(filepath, "w") as f:
                f.write(ref.sha)
            return ref.sha
        except Exception:
            return None

    def load_ref(self, name: str) -> Optional[Ref]:
        filepath: str = os.path.join(self.refs_path, name)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            sha: str = f.read().strip()
        return Ref(name=name, sha=sha)

    def update_ref(self, ref: Ref) -> Optional[str]:
        old: Optional[Ref] = self.load_ref(ref.name)
        self.save_ref(ref)
        return old.sha if old else None

    def delete_ref(self, name: str) -> Optional[str]:
        old: Optional[Ref] = self.load_ref(name)
        if old:
            os.remove(os.path.join(self.refs_path, name))
            return old.sha
        return None

    def list_refs(self) -> Optional[List[Ref]]:
        try:
            return [self.load_ref(f) for f in os.listdir(self.refs_path)]
        except Exception:
            return None

    def log_ref(self, name: str) -> Optional[List[Commit]]:
        ref: Optional[Ref] = self.load_ref(name)
        if not ref:
            return None
        commits: List[Commit] = []
        sha: Optional[str] = ref.sha
        while sha:
            c: Optional[Commit] = self.load_commit(sha)
            if not c:
                break
            commits.append(c)
            sha = c.parents[0] if c.parents else None
        return commits

    def log_refs(self) -> Optional[List[Commit]]:
        seen: dict = {}
        for r in self.list_refs() or []:
            for c in self.log_ref(r.name) or []:
                seen[c.tree] = c
        return list(seen.values())

    def update_head_ref(self, ref: Ref) -> Optional[str]:
        old: Optional[str] = None
        if os.path.exists(self.head_path):
            with open(self.head_path, "r") as f:
                old = f.read().strip()
        with open(self.head_path, "w") as f:
            f.write(ref.sha)
        return old

    def update_index(self, working_tree: Tree) -> Optional[str]:
        sha: Optional[str] = self.save_tree(working_tree)
        if sha:
            with open(self.index_path, "w") as f:
                f.write(sha)
        return sha


# -------------------------------------------------------
# WORKING COPY / CHECKOUT
# -------------------------------------------------------
class WorkingCopy:
    repo: LocalRepository
    work_path: str

    def __init__(self, repo: LocalRepository) -> None:
        self.repo = repo
        self.work_path = repo.work_path

    def checkout(self, commit_sha: str) -> Optional[str]:
        commit: Optional[Commit] = self.repo.load_commit(commit_sha)
        if commit is None:
            return None
        tree: Optional[Tree] = self.repo.load_tree(commit.tree)
        if tree is None:
            return None
        self._clear_working_directory()
        self._restore_tree(tree, self.work_path)
        return commit_sha

    def _clear_working_directory(self) -> None:
        for item in os.listdir(self.work_path):
            if item == ".mg":
                continue
            full: str = os.path.join(self.work_path, item)
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)

    def _restore_tree(self, tree: Tree, path: str) -> None:
        for entry in tree.entries:
            full_path: str = os.path.join(path, entry.name)
            if entry.obj_type == "tree":
                os.makedirs(full_path, exist_ok=True)
                sub_tree: Tree | None = self.repo.load_tree(entry.sha)
                if sub_tree is None:
                    raise ValueError("El tree está corrupto")
                self._restore_tree(sub_tree, full_path)
            elif entry.obj_type == "blob":
                blob: Blob | None = self.repo.load_blob(entry.sha)
                if blob is None:
                    raise ValueError("El blob está corrupto.")
                with open(full_path, "wb") as f:
                    f.write(blob.content)
                if entry.mode & 0o111:
                    os.chmod(full_path, 0o755)
                else:
                    os.chmod(full_path, 0o644)
