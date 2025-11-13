# simple_snapshot.py
from datetime import datetime
from pathlib import Path

from magnesium.interfaces.data_compressor import GzipCompressor

# Asumimos que estas implementaciones existen
from magnesium.interfaces.data_encoder import Utf8Encoder
from magnesium.interfaces.file_store import LocalFileStore
from magnesium.interfaces.object_path_builder import LocalObjectPathBuilder
from magnesium.interfaces.object_repository import (
    LocalObjectRepository,
    ObjectRepository,
)
from magnesium.interfaces.logs_repository import LocalLogRepository, LogRepository
from magnesium.object_values import (
    Blob,
    Commit,
    DirEntry,
    Email,
    FileEntry,
    Sha256Hash,
    Tree,
)


class SimpleSnapshotTool:
    """Herramienta simple para crear snapshots del directorio actual"""

    repo_dir: Path
    repository: ObjectRepository
    log_repo: LogRepository
    work_dir: Path

    def __init__(self, work_dir: str, repo_dir: str = ".mg"):
        self.repo_dir = Path(repo_dir)
        self.work_dir = Path(work_dir)
        encoder = Utf8Encoder()
        compressor = GzipCompressor()
        store = LocalFileStore()
        path_builder = LocalObjectPathBuilder(self.repo_dir / "objects")

        self.repository = LocalObjectRepository(
            self.repo_dir, store, encoder, compressor, path_builder
        )

        self.log_repo = LocalLogRepository(
            self.repo_dir / "logs", store, encoder, path_builder, self.repository
        )

    def initialize_repository(self) -> bool:
        """Inicializa el repositorio si no existe"""
        if not self.repo_dir.exists():
            self.repo_dir.mkdir(parents=True)
            print(f"✅ Repositorio inicializado en: {self.repo_dir}")
            return True
        else:
            print(f"✅ Repositorio ya existe en: {self.repo_dir}")
            return True

    def get_user_input(self) -> tuple[str, str, str]:
        """Obtiene los datos del usuario para el commit"""
        print("\n--- Datos del Commit ---")

        author = input("Autor: ").strip()
        while not author:
            print("❌ El autor es obligatorio")
            author = input("Autor: ").strip()

        email = input("Email: ").strip()
        while not email:
            print("❌ El email es obligatorio")
            email = input("Email: ").strip()

        message = input("Mensaje del commit: ").strip()
        while not message:
            print("❌ El mensaje es obligatorio")
            message = input("Mensaje del commit: ").strip()

        return author, email, message

    def create_blob_from_file(self, file_path: Path) -> Sha256Hash:
        """Crea un blob a partir de un archivo"""
        try:
            assert self.repository is not None
            content = file_path.read_text(encoding="utf-8")
            blob = Blob(content=content)
            return self.repository.save(blob)
        except UnicodeDecodeError:
            # Para archivos binarios, podríamos usar base64, pero por simplicidad los omitimos
            raise ValueError(f"Archivo no es texto UTF-8: {file_path}")

    def build_tree(self, directory: Path) -> Sha256Hash:
        """Construye un tree recursivamente desde un directorio"""
        assert self.repository is not None
        directories: list[DirEntry] = []
        files: list[FileEntry] = []

        # Ordenar para consistencia
        items = sorted(directory.iterdir(), key=lambda x: x.name)

        for item in items:
            if item.name.startswith("."):
                continue  # Ignorar archivos/directorios ocultos

            if item.is_file():
                try:
                    file_hash = self.create_blob_from_file(item)
                    file_mode = 0o644  # Permisos por defecto

                    files.append(
                        FileEntry(name=item.name, mode=file_mode, sha=file_hash)
                    )
                    print(f"  📄 {item.name}")

                except Exception as e:
                    print(f"  ⚠️  Saltando {item.name}: {e}")

            elif item.is_dir():
                # Procesar subdirectorio recursivamente
                subdir_hash = self.build_tree(item)
                dir_mode = 0o755

                directories.append(
                    DirEntry(name=item.name, mode=dir_mode, sha=subdir_hash)
                )
                print(f"  📁 {item.name}/")

        # Crear y guardar el tree
        tree = Tree(directories=directories, files=files)
        return self.repository.save(tree)

    def create_snapshot(self):
        """Crea un snapshot del directorio actual"""
        current_dir = self.work_dir
        print(f"📸 Creando snapshot del directorio: {current_dir}")

        # Obtener datos del usuario
        author, email, message = self.get_user_input()

        # Construir el tree del directorio actual
        print("\n📁 Procesando archivos...")
        tree_hash = self.build_tree(current_dir)
        print(f"✅ Tree creado: {tree_hash.sha[:8]}...")

        # Crear el commit
        commit = Commit(
            author=author,
            email=Email(email),
            message=message,
            date=datetime.now(),
            tree=tree_hash,
            parents=[],  # Por simplicidad, sin padres
        )

        # Guardar el commit
        commit_hash = self.repository.save(commit)
        # Loggear el commit
        self.log_repo.push(commit_hash)
        print(f"✅ Commit creado: {commit_hash.sha}")

        return commit_hash

    def show_history(self):
        """Show commit history"""
        if not self.log_repo:
            print("Log repository not initialized")
            return

        commits = self.log_repo.load()

        print("\n📜 Commit History:")
        print("=" * 80)

        # Mostrar en orden inverso (más reciente primero)
        for i, commit in enumerate(reversed(commits)):
            print(f"\n┌── Commit #{len(commits) - i}")
            print(f"├─ Hash: {self.repository.hash_object(commit).sha}...")
            print(f"├─ Autor: {commit.author} <{commit.email.email}>")
            print(f"├─ Fecha: {commit.date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"└─ Mensaje: {commit.message}")
            print("─" * 80)

    def show_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("📸 SNAPSHOT MENU")
        print("=" * 50)
        print("1. 📷 Crear nuevo snapshot")
        print("2. 📜 Mostrar historial de commits")
        print("0. ❌ Salir")

    def run(self):
        """Ejecuta la herramienta"""
        print("=" * 50)
        print("📸 MAGNESIUM PROJECT")
        print("=" * 50)

        # Inicializar repositorio
        assert self.initialize_repository()

        while True:
            self.show_menu()

            try:
                choice = input("\n👉 Selecciona una opción (0-2): ").strip()

                if choice == "1":
                    # Crear snapshot
                    try:
                        commit_hash = self.create_snapshot()
                        print("\n🎉 ¡Snapshot completado!")
                        print(f"Commit: {commit_hash.sha}")
                        print("Puedes usar este hash para restaurar luego")

                    except Exception as e:
                        print(f"\n❌ Error creando snapshot: {e}")
                        return 1

                elif choice == "2":
                    self.show_history()

                elif choice == "0":
                    print("\n👋 ¡Hasta luego!")
                    break

                else:
                    print("❌ Opción inválida. Por favor selecciona 1-4.")

            except KeyboardInterrupt:
                print("\n\n⚠️  Operación cancelada por el usuario")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

        return 0


def main():
    """Función principal"""
    tool = SimpleSnapshotTool(Path(".mg").parent._str)
    return tool.run()


if __name__ == "__main__":
    exit(main())
