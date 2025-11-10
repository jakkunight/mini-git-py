from dataclasses import dataclass
from re import fullmatch


@dataclass
class Email:
    email: str

    def __post_init__(self):
        try:
            assert fullmatch(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", self.email
            ), "El email ingresado no es válido!"
        except Exception as e:
            print(e)
