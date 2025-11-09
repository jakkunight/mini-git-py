import os
from magnesium.controllers.local_repository import LocalRepository
from magnesium.models.blob import Blob
from magnesium.models.commit import Commit
from magnesium.models.tree import Tree, BlobEntry
from magnesium.models.references import Ref


def test_repository_init():
    repo = LocalRepository()
    result = repo.init(str("/home/jakku/magnesium"))
    assert result == str("/home/jakku/magnesium")
    assert os.path.exists("/home/jakku/magnesium/.mg")
    assert os.path.exists("/home/jakku/magnesium/.mg/objects")
    assert os.path.exists("/home/jakku/magnesium/.mg/refs")


def test_save_and_load_blob():
    repo = LocalRepository()
    repo.init(str("/home/jakku/magnesium"))

    blob = Blob("contenido de prueba", "blob")
    sha = repo.save_blob(blob)
    assert sha is not None

    loaded = repo.load_blob(sha)
    assert loaded is not None
    assert loaded.content == blob.content
    assert loaded.type == "blob"


def test_save_and_load_tree():
    repo = LocalRepository()
    repo.init(str("/home/jakku/magnesium"))

    blob = Blob("hola", "blob")
    blob_sha = repo.save_blob(blob)

    assert blob_sha is not None

    tree = Tree([], [BlobEntry(100644, "hola.txt", blob_sha)])
    tree_sha = repo.save_tree(tree)

    assert tree_sha is not None

    loaded = repo.load_tree(tree_sha)
    assert loaded is not None
    assert len(loaded.blob_entries) == 1
    assert loaded.blob_entries[0].name == "hola.txt"


def test_save_and_load_commit():
    repo = LocalRepository()
    repo.init(str("/home/jakku/magnesium"))

    blob = Blob("hola", "blob")
    blob_sha = repo.save_blob(blob)
    assert blob_sha is not None
    tree = Tree([], [BlobEntry(100644, "hola.txt", blob_sha)])
    tree_sha = repo.save_tree(tree)
    assert tree_sha is not None

    commit = Commit("Autor", "mail@example.com", "msg", "2025-01-01", [], tree_sha)
    commit_sha = repo.save_commit(commit)

    assert commit_sha is not None

    loaded = repo.load_commit(commit_sha)
    assert loaded is not None
    assert loaded.author == commit.author
    assert loaded.message == commit.message


def test_save_and_load_ref():
    repo = LocalRepository()
    repo.init(str("/home/jakku/magnesium"))
    blob = Blob("hola", "blob")
    blob_sha = repo.save_blob(blob)
    assert blob_sha is not None
    tree = Tree([], [BlobEntry(100644, "hola.txt", blob_sha)])
    tree_sha = repo.save_tree(tree)
    assert tree_sha is not None

    commit = Commit("Autor", "mail@example.com", "msg", "2025-01-01", [], tree_sha)
    commit_sha = repo.save_commit(commit)

    assert commit_sha is not None

    loaded = repo.load_commit(commit_sha)
    assert loaded is not None
    assert loaded.author == commit.author
    assert loaded.message == commit.message

    ref = Ref("main", commit_sha, "commit")
    result = repo.save_ref(ref)
    assert result is not None
    assert result == ref.sha

    loaded = repo.load_ref("main")
    assert loaded is not None
    assert loaded.name == ref.name
    assert loaded.sha == ref.sha
    assert loaded.type == ref.type
