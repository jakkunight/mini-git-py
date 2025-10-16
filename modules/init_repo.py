import os


def init():
    """
    Inicializa el repositorio.
    """
    # Crea el repositorio:
    print("Iniciando repositorio en " + os.getcwd())
    os.mkdir(".mini-git-py")
    # Crea la carpeta `objects` para poder almacenar los objetos:
    os.mkdir(".mini-git-py/objects")
    # Crear un archivo `index` para almacenar los cambios a commitear:
    index = open(".mini-git-py/index", "wt")
    index.close()
