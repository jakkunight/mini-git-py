import os
import shutil
from typing import Optional

from magnesium.models.version_control_system import VersionControlSystem
from magnesium.models.tree import Tree, TreeEntry, BlobEntry
from magnesium.models.blob import Blob


class Magnesium(VersionControlSystem):
   
    def _ensure_work_path(self, repository) -> str:
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

        Ajustado a la estructura actual de modelos: Tree tiene `tree_entries`
        y `blob_entries`. TreeEntry/BlobEntry contienen (mode, name, sha).
        """
        tree = repository.load_tree(tree_sha)
        assert tree is not None, f"Tree {tree_sha} no existe en el repositorio"

        os.makedirs(target_path, exist_ok=True)

        expected_names = {e.name for e in getattr(tree, "blob_entries", [])} | {
            e.name for e in getattr(tree, "tree_entries", [])
        }
        self._sync_directory_with_tree(target_path, expected_names)

        for te in getattr(tree, "tree_entries", []):
            if te.name == ".mg":
                continue
            entry_path = os.path.join(target_path, te.name)
            self._restore_tree(repository, te.sha, entry_path)

        for be in getattr(tree, "blob_entries", []):
            if be.name == ".mg":
                continue
            entry_path = os.path.join(target_path, be.name)
            blob = repository.load_blob(be.sha)
            assert blob is not None, f"Blob {be.sha} no existe"
            content = getattr(blob, "content", b"")
            if isinstance(content, str):
                content = content.encode()
            with open(entry_path, "wb") as f:
                f.write(content)
            try:
                os.chmod(entry_path, be.mode)
            except Exception:
                pass

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
        try:
            self._restore_tree(repository, c.tree, work_path)
        except AssertionError:
            raise
        except Exception:
            return None

        return commit

    def checkout_ref(self, repository, name: str) -> Optional[str]:
        """
        Restaurar por nombre de referencia (branch/ref).
        """
        assert name and isinstance(name, str), "Nombre de ref inválido"
        ref = repository.load_ref(name)
        if ref is None:
            return None
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

    def _file_mode(self, path: str) -> int:
        try:
            return os.stat(path).st_mode
        except Exception:
            return 0o100644

    def _find_tree_entry(self, tree: Tree, name: str):
        for e in getattr(tree, "tree_entries", []):
            if e.name == name:
                return e
        return None

    def _find_blob_entry(self, tree: Tree, name: str):
        for e in getattr(tree, "blob_entries", []):
            if e.name == name:
                return e
        return None

    def stage_file(self, repository, path: str) -> str | None:
        """
        Añade un archivo al staging area del repositorio dado. Actualiza el tree.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError`.
        """
        assert path and isinstance(path, str), "Ruta inválida"

        work_path = self._ensure_work_path(repository)
        abs_path = path if os.path.isabs(path) else os.path.join(work_path, path)
        abs_path = os.path.abspath(abs_path)
        assert os.path.exists(abs_path) and os.path.isfile(abs_path), "Archivo no existe"

        rel = os.path.relpath(abs_path, work_path)
        parts = rel.split(os.sep)
        if ".mg" in parts:
            return None

        with open(abs_path, "rb") as f:
            content = f.read()

        blob = Blob(content=content)
        blob_sha = repository.save_blob(blob)
        assert blob_sha is not None, "No se pudo guardar el blob"

        file_mode = self._file_mode(abs_path)
        filename = parts[-1]

        index_tree = repository.load_index()
        if index_tree is None:
            be = BlobEntry(mode=file_mode, name=filename, sha=blob_sha)
            new_index = Tree(tree_entries=[], blob_entries=[be])
            res = repository.update_index(new_index)
            assert res is not None, "No se pudo actualizar el índice"
            return res

        if len(parts) == 1:
            existing = self._find_blob_entry(index_tree, filename)
            if existing:
                index_tree.blob_entries = [
                    be for be in index_tree.blob_entries if be.name != filename
                ]
            index_tree.tree_entries = [
                te for te in index_tree.tree_entries if te.name != filename
            ]
            be = BlobEntry(mode=file_mode, name=filename, sha=blob_sha)
            index_tree.blob_entries.append(be)
            res = repository.update_index(index_tree)
            assert res is not None, "No se pudo actualizar el índice"
            return res

        parent_dirs = parts[:-1]

        ancestors: list[tuple[Tree, str, object]] = []
        current = index_tree
        missing_from = None
        for idx, d in enumerate(parent_dirs):
            entry = self._find_tree_entry(current, d)
            ancestors.append((current, d, entry))
            if entry:
                loaded = repository.load_tree(entry.sha)
                assert loaded is not None, f"Tree {entry.sha} referenciado no existe"
                current = loaded
            else:
                missing_from = idx
                break

        leaf_blob_entry = BlobEntry(mode=file_mode, name=filename, sha=blob_sha)

        if missing_from is None:
            current.blob_entries = [be for be in current.blob_entries if be.name != filename]
            current.tree_entries = [te for te in current.tree_entries if te.name != filename]
            current.blob_entries.append(leaf_blob_entry)
            child_sha = repository.save_tree(current)
            assert child_sha is not None, "No se pudo guardar el árbol modificado"
            for anc_tree, anc_name, anc_entry in reversed(ancestors[:-1]):
                if anc_entry:
                    for te in anc_tree.tree_entries:
                        if te.name == anc_name:
                            te.sha = child_sha
                            break
                    child_sha = repository.save_tree(anc_tree)
                    assert child_sha is not None, "No se pudo guardar el árbol ancestro"
            if ancestors:
                root_tree = index_tree
                first_anc = ancestors[0]
                root_dir = first_anc[1]
                found = False
                for te in root_tree.tree_entries:
                    if te.name == root_dir:
                        te.sha = child_sha
                        found = True
                        break
                if not found:
                    root_tree.tree_entries.append(TreeEntry(mode=0o40000, name=root_dir, sha=child_sha))
                res = repository.update_index(root_tree)
                assert res is not None, "No se pudo actualizar el índice"
                return res
            else:
                res = repository.update_index(index_tree)
                assert res is not None, "No se pudo actualizar el índice"
                return res

        missing_dirs = parent_dirs[missing_from:]
        child_sha = None
        child_name = None
        for d in reversed(missing_dirs):
            if child_sha is None:
                new_tree = Tree(tree_entries=[], blob_entries=[leaf_blob_entry])
            else:
                te = TreeEntry(mode=0o40000, name=child_name, sha=child_sha)
                new_tree = Tree(tree_entries=[te], blob_entries=[])
            new_sha = repository.save_tree(new_tree)
            assert new_sha is not None, "No se pudo guardar un árbol intermedio"
            child_sha = new_sha
            child_name = d

        if ancestors:
            parent_idx = missing_from - 1
            if parent_idx >= 0:
                parent_tree, parent_dir, parent_entry = ancestors[parent_idx]
                found = False
                for te in parent_tree.tree_entries:
                    if te.name == missing_dirs[0]:
                        te.sha = child_sha
                        found = True
                        break
                if not found:
                    parent_tree.tree_entries.append(TreeEntry(mode=0o40000, name=missing_dirs[0], sha=child_sha))
                child_sha = repository.save_tree(parent_tree)
                assert child_sha is not None, "No se pudo guardar árbol padre existente"
                for anc_tree, anc_name, anc_entry in reversed(ancestors[:parent_idx]):
                    for te in anc_tree.tree_entries:
                        if te.name == anc_name:
                            te.sha = child_sha
                            break
                    child_sha = repository.save_tree(anc_tree)
                    assert child_sha is not None, "No se pudo guardar el árbol ancestro"
                root_tree = index_tree
                first_dir = ancestors[0][1] if ancestors else missing_dirs[0]
                found = False
                for te in root_tree.tree_entries:
                    if te.name == first_dir:
                        te.sha = child_sha
                        found = True
                        break
                if not found:
                    root_tree.tree_entries.append(TreeEntry(mode=0o40000, name=first_dir, sha=child_sha))
                res = repository.update_index(root_tree)
                assert res is not None, "No se pudo actualizar el índice"
                return res

        found = False
        first_missing = missing_dirs[0]
        for te in index_tree.tree_entries:
            if te.name == first_missing:
                te.sha = child_sha
                found = True
                break
        if not found:
            index_tree.tree_entries.append(TreeEntry(mode=0o40000, name=first_missing, sha=child_sha))
        res = repository.update_index(index_tree)
        assert res is not None, "No se pudo actualizar el índice"
        return res

    def stage_directory(self, repository, path: str) -> str | None:
        """
        Añade un archivo al staging area del repositorio dado. Actualiza el index del repositorio con las entradas de un directorio. Devuelve SHA-256 del `Tree` creado.
        """
        assert path and isinstance(path, str), "Ruta inválida"
        work_path = self._ensure_work_path(repository)
        abs_path = path if os.path.isabs(path) else os.path.join(work_path, path)
        abs_path = os.path.abspath(abs_path)
        assert os.path.exists(abs_path) and os.path.isdir(abs_path), "Directorio no existe"

        # recorrer todos los archivos (excluyendo .mg) y stagearlos
        for root, dirs, files in os.walk(abs_path):
            # evitar indexar .mg internals
            if ".mg" in root.split(os.sep):
                continue
            for f in files:
                if f == ".mg":
                    continue
                file_abs = os.path.join(root, f)
                rel = os.path.relpath(file_abs, work_path)
                res = self.stage_file(repository, rel)
                assert res is not None, f"No se pudo stagear {rel}"

        # intentar devolver el SHA del tree correspondiente al directorio solicitado
        rel_dir = os.path.relpath(abs_path, work_path)
        if ".mg" in rel_dir.split(os.sep):
            return None
        if rel_dir == ".":
            idx_tree = repository.load_index()
            assert idx_tree is not None, "Índice no disponible"
            res = repository.update_index(idx_tree)
            assert res is not None, "No se pudo actualizar el índice"
            return res
        parts = rel_dir.split(os.sep)
        idx_tree = repository.load_index()
        assert idx_tree is not None, "Índice no disponible"
        cur = idx_tree
        entry = None
        for p in parts:
            entry = self._find_tree_entry(cur, p)
            if entry is None:
                return None
            cur = repository.load_tree(entry.sha)
            if cur is None:
                return None
        # si llegamos aquí, `entry.sha` es el tree buscado
        return entry.sha

