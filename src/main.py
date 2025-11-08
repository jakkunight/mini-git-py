from datetime import datetime, timezone
from magnesium.controllers.local_repository import LocalRepository
from magnesium.models.blob import Blob
from magnesium.models.commit import Commit
from magnesium.models.tree import BlobEntry, Tree


def main() -> int:
    repo = LocalRepository("/home/jakku/magnesium")
    _ = repo.init("/home/jakku/magnesium")
    blob = Blob(0o100644, "Hello World!".encode("utf-8"))
    blob_hash = repo.save_blob(blob)
    if blob_hash is None:
        return 1
    blob_entry = BlobEntry(0o100644, "hello.txt", blob_hash)
    tree = Tree([], [blob_entry])
    tree_hash = repo.save_tree(tree)
    if tree_hash is None:
        return 2
    commit = Commit(
        "Santiago Wu",
        "santiago.wu.chamorro@gmail.com",
        "Hello World",
        str(datetime.now(timezone.utc)),
        [],
        tree_hash,
    )
    commit_hash = repo.save_commit(commit)
    if commit_hash is None:
        return 3

    print(f"Commit hash: {commit_hash}")
    return 0


if __name__ == "__main__":
    exit(main())
