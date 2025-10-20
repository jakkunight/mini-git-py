import os
from os.path import join, exists, isdir, isfile


class TreeEntry:
    """
    Una clase que representa una entrada en el `Tree`.
    """

    def __init__(self, permissions: int, entry_name: str, entry_hash: str):
        # TODO:
        # Mejorar la validación de permisos del archivo:
        if permissions is None or permissions == 0:
            raise TypeError("El dato provisto no es un permiso UNIX válido!")

        final_path = join(self.dirpath, entry_name)
        if not exists(final_path):
            raise TypeError("El nombre de archivo provisto no existe!")

        if isdir(final_path):
            self.type = "tree"

        if isfile(final_path):
            self.type = "blob"

        # TODO:
        # Validar el hash ingresado.
        object_dir: str = ""
        object_filename: str = ""
        entry_dir = entry_hash[0:2]
        entry_filename = entry_hash[2:]


class Tree:
    def __init__(self, path: str):
        if path == "" or path is None:
            raise TypeError("La ruta provista está vacía!")

        if not exists(path):
            raise FileNotFoundError("La ruta provista no existe!")

        if not isdir(path):
            raise IsADirectoryError("La ruta provista no es un directorio!")

        self.dirpath = path

    # TODO:
    # Implementar la función para añadir entradas al árbol.
    def add_blob(self):
        pass
