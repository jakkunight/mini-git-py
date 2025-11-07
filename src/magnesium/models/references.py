from dataclasses import dataclass
import re


@dataclass
class Ref:
    """
    Una clase que representa una referencia mutable a un `Commit` o un `Tag`.
    """

    name: str
    sha: str
    type: str = "commit"

    def __post_init__(self):
        assert self.name != "", """
            El nombre de la referencia no puede estar vacío.
        """
        assert re.match(r"^[a-f0-9]{64}$", self.sha), f"""
            El hash provisto es inválido.

            Valor provisto:
            - {self.sha}
        """

        assert self.type in ("commit", "tag"), f"""
            El tipo de referencia provisto es inválido.

            Valores permitidos:
            - "commit"
            - "tag"

            Valor provisto:
            - {self.type}
        """
