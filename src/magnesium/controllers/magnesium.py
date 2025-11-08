import os
import shutil
from typing import Optional

from magnesium.models.version_control_system import VersionControlSystem


class Magnesium(VersionControlSystem):
   
    def _ensure_work_path(self, repository) -> str:
        # Under-spec: asumimos que la implementación concreta (LocalRepository)
        # expone `work_path`. Si no, usamos el cwd.
        return getattr(repository, "work_path", os.getcwd())

    def _sync_directory_with_tree(self, path: str, entry_names: set[str]) -> None:
        """Quita del filesystem los archivos/dirs presentes en `path` que
        no aparecen en `entry_names`. Preserva la carpeta `.mg`.
        """
        for name in os.listdir(path):
            if name == ".mg":
                continue
            if name not in entry_names:
                full = os.path.join(path, name)
                if os.path.isdir(full) and not os.path.islink(full):
                    shutil.rmtree(full)
                else:
                    os.remove(full)

    def _restore_tree(self, repository, tree_sha: str, target_path: str) -> None:
        """Restaura recursivamente el `Tree` identificado por `tree_sha`
        en la carpeta `target_path`.
        """
        tree = repository.load_tree(tree_sha)
        assert tree is not None, f"Tree {tree_sha} no existe en el repositorio"

        os.makedirs(target_path, exist_ok=True)

        # nombres esperados para sincronizar
        expected_names = {e.name for e in tree.entries}
        # eliminar entradas no presentes
        self._sync_directory_with_tree(target_path, expected_names)

        for entry in tree.entries:
            entry_path = os.path.join(target_path, entry.name)
            if entry.obj_type == "tree":
                # directorio: recrear recursivamente
                self._restore_tree(repository, entry.sha, entry_path)
            elif entry.obj_type == "blob":
                blob = repository.load_blob(entry.sha)
                assert blob is not None, f"Blob {entry.sha} no existe"
                # escribir contenido
                with open(entry_path, "wb") as f:
                    f.write(blob.content)
                try:
                    os.chmod(entry_path, blob.mode)
                except Exception:
                    # no crítico en entornos Windows o si no tenemos permisos
                    pass
            else:
                raise AssertionError(f"Tipo de entrada desconocido: {entry.obj_type}")

    def checkout_commit(self, repository, commit: str) -> Optional[str]:
        """
        Restaurar el working directory al estado del `commit`.
        Devuelve el SHA-256 del commit restaurado o None en caso de fallo.
        """
        assert commit and isinstance(commit, str), "Commit SHA inválido"
        assert len(commit) == 64, "Commit SHA inválido"

        c = repository.load_commit(commit)
        if c is None:
            return None

        work_path = self._ensure_work_path(repository)
        # restaurar árbol asociado al commit
        try:
            self._restore_tree(repository, c.tree, work_path)
        except AssertionError:
            raise
        except Exception:
            return None

        # opcional: actualizar index / HEAD no lo hacemos aquí; sólo restauramos WD
        return commit

    def checkout_ref(self, repository, name: str) -> Optional[str]:
        """
        Restaurar por nombre de referencia (branch/ref).
        """
        assert name and isinstance(name, str), "Nombre de ref inválido"
        ref = repository.load_ref(name)
        if ref is None:
            return None
        # ref.sha apunta al commit
        return self.checkout_commit(repository, ref.sha)

    def checkout_tag(self, repository, name: str) -> Optional[str]:
        """
        Restaurar por nombre de tag.
        """
        assert name and isinstance(name, str), "Nombre de tag inválido"
        tag = repository.load_tag(name)
        if tag is None:
            return None
        return self.checkout_commit(repository, tag.commit)

