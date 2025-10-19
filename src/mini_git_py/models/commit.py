from mini_git_py.models.author import Author
from datetime import datetime, timezone


class Commit:
    """
    Una clase que representa los datos de un commit de forma
    estructurada.
    """

    def __init__(self, author: Author, message: str):
        # NOTE:
        # El tipo `Author` ya provee validación propia.
        # No es necesario validarlo aquí.
        self.author = author

        # NOTE:
        # El mensaje provisto NO puede ser vacío
        if message == "":
            raise TypeError("Debes especificar un mensaje para el commit!")
            return

        self.message = message

        # NOTE:
        # La fecha y hora deben ser autogeneradas
        self.date: str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        # TODO:
        # Falta implementar el sistema para hallar el commit actual y el tree actual.
