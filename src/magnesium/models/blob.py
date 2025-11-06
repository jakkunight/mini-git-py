from dataclasses import dataclass


@dataclass
class Blob:
    """
    Una clase que representa el contenido de un archivo sin ningún metadato. Sus campos pueden estar vacíos, a excepción del tipo, que es constante.
    """

    name: str
    mode: int
    content: bytes
    type = "blob"

    def __post_init__(self):
        assert self.type == "type", """
            El tipo del blob es constante y no debe ser modificado!
        """
