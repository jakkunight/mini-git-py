class Author:
    """
    Una clase que representa el autor de un commit.
    Requiere dos campos:
    + `name`: Repressenta el nombre del autor con un `str`. No puede ser nulo o vacío.
    + `email`: Representa un email del autor con un `str`. No puede ser nulo o vacío.
    """

    def __init__(self, name: str, email: str):
        if name == "":
            raise TypeError("Name is an empty string! Please provide a name.")
            return

        if email == "":
            raise TypeError("Email is an empty string! Please provide a valid email.")
            return

        self.name = name
        self.email = email
