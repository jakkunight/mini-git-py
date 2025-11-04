from dataclasses import dataclass
import re


@dataclass
class Ref:
    name: str
    sha: str

    def __post_init__(self):
        assert self.name != "", """
            El nombre de la referencia no puede estar vacío.
        """
        assert re.match(r"^[a-f0-9]{64}$", self.sha), f"""
            El hash provisto es inválido.

            Valor provisto:
            - {self.sha}
        """
