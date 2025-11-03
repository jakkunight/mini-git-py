class Author:
    def __init__(self, name: str, email: str):
        if name is None or name == "":
            raise TypeError("El nombre provisto no puede ser vacío.")
        if email is None or email == "":
            raise TypeError("El email provisto no puede ser vacío.")
