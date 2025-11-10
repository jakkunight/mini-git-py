from dataclasses import dataclass
from re import fullmatch


@dataclass
class Sha256Hash:
    sha: str

    def __post_init__(self):
        try:
            assert fullmatch(r"[0-9a-f]{64}", self.sha), (
                "El formato del hash es inválido. Un hash string sólo puede contener dígitos hexadecimales y debe ser de 256 bits de longitud."
            )
        except Exception as e:
            print(e)
