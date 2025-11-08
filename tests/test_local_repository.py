from magnesium.controllers.local_repository import LocalRepository
from magnesium.models.blob import Blob
from magnesium.models.tree import Tree, BlobEntry, TreeEntry
from magnesium.models.commit import Commit
from magnesium.models.references import Ref
from time import time


def main():
    repo = LocalRepository()
    _ = repo.init("/home/jakku/magnesium")

    print("Repo inicializado.")

    # 1. Guardar un blob
    blob = Blob("Hola mundo\n")
    blob_sha = repo.save_blob(blob)
    if blob_sha is None:
        print("An error occurred when saving the Blob.")
        return
    print("Blob:", blob_sha)

    # 2. Crear un árbol (un archivo en el directorio)
    entry = BlobEntry(0o100644, "hola.txt", blob_sha)
    tree = Tree([], [entry])
    tree_sha = repo.save_tree(tree)
    assert tree_sha is not None
    print("Tree:", tree_sha)

    # 3. Crear commit
    commit = Commit(
        author="Juan",
        email="juan@example.com",
        message="Primer commit",
        date=str(int(time())),
        parents=[],
        tree=tree_sha,
    )
    commit_sha = repo.save_commit(commit)
    assert commit_sha is not None
    print("Commit:", commit_sha)

    # 4. Guardar referencia "main"
    ref = Ref("main", commit_sha, "commit")
    repo.save_ref(ref)
    print("Ref creada: main →", commit_sha)

    # 5. Log de la referencia
    commits = repo.log_ref("main")
    assert commits is not None
    print("Log de main:")
    for c in commits:
        print("  -", c.message)

    # 6. Cargar commit desde SHA
    loaded = repo.load_commit(commit_sha)
    print("Commit cargado:", loaded)

    # 7. Ver el index
    repo.update_index(tree)
    loaded_index = repo.load_index()
    print("Index cargado:", loaded_index)


if __name__ == "__main__":
    main()
