from pathlib import Path
from magnesium.interfaces.data_compressor import GzipCompressor
from magnesium.interfaces.data_encoder import Utf8Encoder
from magnesium.interfaces.file_store import LocalFileStore
from magnesium.interfaces.object_path_builder import LocalObjectPathBuilder
from magnesium.interfaces.object_repository import LocalObjectRepository
from magnesium.object_values.email import Email

base_dir = Path("/home/jakku/magnesium/.mg")
compressor = GzipCompressor()
encoder = Utf8Encoder()
local_file_store = LocalFileStore()
path_builder = LocalObjectPathBuilder(base_dir)
repo = LocalObjectRepository(
    base_dir,
    local_file_store,
    encoder,
    compressor,
    path_builder,
)


def main():
    while True:
        print("\x1b[2J\x1b[0H")
        print(" " * 4 + "-" * 4 + " Magnesium Version Control System " + "-" * 4 + "\n")
        print("Opciones:")
        print("\t1. Crear snapshot del directorio")
        print("\t0. Salir")
        print("\n")
        try:
            opcode = int(input("Ingrese su opción> "))
        except Exception:
            continue
        match opcode:
            case 0:
                print("Sayonara!")
                break
            case 1:
                print("==== Datos del Autor ====")
                while True:
                    author = input("Ingresa tu nombre: ")
                    if author != "":
                        break
                email = ""
                while True:
                    try:
                        email = Email(input("Ingresa tu email: "))
                        break
                    except Exception:
                        continue

                print("Creando snapshot...")
                print("Snapshot creado correctamente")
                _ = input("Presione ENTER para continuar...")
            case _:
                continue


if __name__ == "__main__":
    main()
