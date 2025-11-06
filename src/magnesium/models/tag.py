from dataclasses import dataclass
from re import match


@dataclass
class Tag:
    name: str
    message: str
    commit: str
    type = "tag"

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """
        assert match(r"^[a-f0-9]{64}$`", self.commit), f"""
            El commit referenciado es incorrecto.

            Valor provisto:
            - {self.commit}
        """
