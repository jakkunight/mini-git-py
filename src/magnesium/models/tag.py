from dataclasses import dataclass
from re import match


@dataclass
class Tag:
    """
    Una clase que representa un tag inmutable para un `Commit`.
    Se usa generalmente para almacenar más información sobre un `Commit` o anotar lanzamientos de versione importantes.
    """

    name: str
    message: str
    commit: str
    type: str = "tag"

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede estar vacío.
        """
        assert match(r"^[a-f0-9]{64}$`", self.commit), f"""
            El commit referenciado es incorrecto.

            Valor provisto:
            - {self.commit}
        """
        assert self.type == "tag", """
            El tipo de este objeto debe ser siempre "tag"!
        """
