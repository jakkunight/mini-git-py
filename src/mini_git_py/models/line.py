class AddedLine:
    """
    Una clase que representa una línea añadida.
    """

    def __init__(self, position: int, content: str):
        if content is None or content == "":
            raise TypeError("La línea no puede estar vacía!")
            return
        if position < 0:
            raise TypeError("El número de línea no puede ser menor a cero!")
            return

        self.content = content
        self.position = position


class DeletedLine:
    """
    Una clase que representa una línea eliminada.
    """

    def __init__(self, position: int, content: str):
        if content is None or content == "":
            raise TypeError("La línea no puede estar vacía!")
            return
        if position < 0:
            raise TypeError("El número de línea no puede ser menor a cero!")
            return

        self.content = content
        self.position = position
