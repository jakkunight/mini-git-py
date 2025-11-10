# WARN:
# Este código ha sido generado con asistencia de IA (GPT-5).
# Implementa la interfaz `VersionControlSystem` para operar sobre
# un repositorio local (`LocalRepository`), gestionando commits,
# árboles, blobs, ramas y tags de forma simple y modular.

import os
from datetime import datetime
from mini_git_py.models.local_repository import LocalRepository
from mini_git_py.models.commit import Commit
from mini_git_py.models.references import Ref
from mini_git_py.models.tag import Tag
from mini_git_py.models.tree import Tree, TreeEntry
from .version_control_system import VersionControlSystem


class LocalVersionControlSystem(VersionControlSystem):
    """
    Implementación local del sistema de control de versiones.
    Coordina las operaciones de `LocalRepository` sin sobrecargarlo.
    """

    # --------------------------------------------------------
    # Inicialización del repositorio
    # --------------------------------------------------------
    def init(self, repository: LocalRepository) -> str | None:
        try:
            repo_path = repository.init()
            return repo_path
        except Exception as e:
            raise AssertionError(f"Error al inicializar el repositorio: {e}")

    # --------------------------------------------------------
    # Añadir un archivo individual al staging area
    # --------------------------------------------------------
    def stage_file(self, repository: LocalRepository, path: str) -> str | None:
        try:
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                raise AssertionError(f"El archivo {path} no existe.")

            with open(abs_path, "rb") as f:
                content = f.read()

            blob = repository.save_blob_from_path(abs_path, content)
            if not blob:
                raise AssertionError("No se pudo guardar el blob.")

            # Crear un árbol temporal de un solo archivo y actualizar índice
            entry = TreeEntry(mode=100644, name=os.path.basename(path), sha=blob, obj_type="blob")
            tree = Tree(name="staged", entries=[entry])
            repository.update_index(tree)
            return blob
        except Exception as e:
            raise AssertionError(f"Error al añadir archivo al staging area: {e}")

    # --------------------------------------------------------
    # Añadir un directorio completo al staging area
    # --------------------------------------------------------
    def stage_directory(self, repository: LocalRepository, path: str) -> str | None:
        try:
            abs_path = os.path.abspath(path)
            if not os.path.isdir(abs_path):
                raise AssertionError(f"{path} no es un directorio válido.")

            entries = []
            for root, _, files in os.walk(abs_path):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    with open(full_path, "rb") as f:
                        content = f.read()
                    blob_sha = repository.save_blob_from_path(full_path, content)
                    rel_path = os.path.relpath(full_path, abs_path)
                    entries.append(TreeEntry(mode=100644, name=rel_path, sha=blob_sha, obj_type="blob"))

            tree = Tree(name=os.path.basename(abs_path), entries=entries)
            repository.update_index(tree)
            return repository.save_tree(tree)
        except Exception as e:
            raise AssertionError(f"Error al añadir directorio al staging area: {e}")

    # --------------------------------------------------------
    # Crear un commit desde el staging area (index)
    # --------------------------------------------------------
    def commit(self, repository: LocalRepository, author: str, email: str, message: str) -> str | None:
        try:
            # Cargar árbol desde el índice
            index_data = repository._load_raw_from_index()
            if not index_data:
                raise AssertionError("No hay archivos en el staging area.")

            _, body = index_data
            tree_sha = repository._save_raw("tree", body)

            # Obtener commit padre (si existe)
            head_ref = repository.load_ref("main")
            parent = head_ref.sha if head_ref else None

            commit = Commit(
                tree=tree_sha,
                parents=[parent] if parent else [],
                author=author,
                email=email,
                message=message,
                date=datetime.now().isoformat(),
            )

            commit_sha = repository.save_commit(commit)
            if not commit_sha:
                raise AssertionError("No se pudo guardar el commit.")

            # Actualizar HEAD y limpiar índice
            repository.save_ref(Ref("main", commit_sha))
            repository.update_head_ref(Ref("main", commit_sha))
            repository.clear_index()
            return commit_sha
        except Exception as e:
            raise AssertionError(f"Error al crear commit: {e}")

    # --------------------------------------------------------
    # Restaurar un commit específico
    # --------------------------------------------------------
    def checkout_commit(self, repository: LocalRepository, commit: str) -> str | None:
        try:
            c = repository.load_commit(commit)
            if not c:
                raise AssertionError("Commit no encontrado.")

            tree = repository.load_tree(c.tree)
            if not tree:
                raise AssertionError("Árbol del commit no encontrado.")

            for entry in tree.entries:
                blob = repository.load_blob(entry.sha)
                file_path = os.path.join(repository.work_path, entry.name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(blob.content)

            repository.update_head_ref(Ref("main", commit))
            return commit
        except Exception as e:
            raise AssertionError(f"Error al restaurar commit: {e}")

    # --------------------------------------------------------
    # Restaurar desde una referencia (rama)
    # --------------------------------------------------------
    def checkout_ref(self, repository: LocalRepository, name: str) -> str | None:
        ref = repository.load_ref(name)
        if not ref:
            raise AssertionError(f"La referencia {name} no existe.")
        return self.checkout_commit(repository, ref.sha)

    # --------------------------------------------------------
    # Restaurar desde un tag
    # --------------------------------------------------------
    def checkout_tag(self, repository: LocalRepository, name: str) -> str | None:
        tag = repository.load_tag(name)
        if not tag:
            raise AssertionError(f"El tag {name} no existe.")
        return self.checkout_commit(repository, tag.commit)

    # --------------------------------------------------------
    # Mostrar historial de commits
    # --------------------------------------------------------
    def log(self, repository: LocalRepository, ref: Ref | None = None):
        name = ref.name if ref else "main"
        commits = repository.log_ref(name)
        return commits if commits else []

    # --------------------------------------------------------
    # Crear nueva rama
    # --------------------------------------------------------
    def create_branch(self, repository: LocalRepository, name: str, commit: str | None) -> Ref | None:
        try:
            c_sha = commit or repository.load_ref("main").sha
            ref = Ref(name, c_sha)
            repository.save_ref(ref)
            return ref
        except Exception as e:
            raise AssertionError(f"Error al crear rama {name}: {e}")

    # --------------------------------------------------------
    # Eliminar rama
    # --------------------------------------------------------
    def delete_branch(self, repository: LocalRepository, name: str) -> str | None:
        try:
            sha = repository.delete_ref(name)
            return sha
        except Exception as e:
            raise AssertionError(f"Error al eliminar rama {name}: {e}")

    # --------------------------------------------------------
    # Listar ramas
    # --------------------------------------------------------
    def list_branches(self, repository: LocalRepository) -> list[Ref] | None:
        return repository.list_refs()

    # --------------------------------------------------------
    # Crear tag
    # --------------------------------------------------------
    def create_tag(self, repository: LocalRepository, name: str, commit: str | None) -> Tag | None:
        try:
            c_sha = commit or repository.load_ref("main").sha
            tag = Tag(name=name, commit=c_sha)
            repository.save_tag(tag)
            return tag
        except Exception as e:
            raise AssertionError(f"Error al crear tag {name}: {e}")

    # --------------------------------------------------------
    # Eliminar tag
    # --------------------------------------------------------
    def delete_tag(self, repository: LocalRepository, name: str) -> str | None:
        return repository.delete_ref(name)

    # --------------------------------------------------------
    # Listar tags
    # --------------------------------------------------------
    def list_tags(self, repository: LocalRepository) -> list[Tag] | None:
        try:
            tags = []
            for f in os.listdir(repository.refs_path):
                if f.startswith("tag_"):
                    tag = repository.load_tag(f)
                    if tag:
                        tags.append(tag)
            return tags
        except Exception as e:
            raise AssertionError(f"Error al listar tags: {e}")

    # --------------------------------------------------------
    # Mostrar diferencias entre commits (simplificada)
    # --------------------------------------------------------
    def diff_commits(self, repository: LocalRepository, base: str | None, target: str) -> list[str] | None:
        try:
            target_commit = repository.load_commit(target)
            base_commit = repository.load_commit(base) if base else None
            diffs = []
            if not base_commit:
                diffs.append(f"Nuevo commit creado: {target_commit.message}")
            else:
                diffs.append(f"Cambios entre {base[:7]} y {target[:7]}:\n")
                diffs.append(f"- {target_commit.message}")
            return diffs
        except Exception as e:
            raise AssertionError(f"Error al calcular diferencias: {e}")
