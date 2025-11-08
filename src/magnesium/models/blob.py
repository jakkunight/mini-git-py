from dataclasses import dataclass


@dataclass
class Blob:
    """
    Una clase que representa el contenido de un archivo sin ningún metadato. Sus campos pueden estar vacíos, a excepción del tipo, que es constante.
    """

    content: str
    type: str = "blob"

    def __post_init__(self):
        assert self.type == "blob", """
            El tipo del blob es constante y no debe ser modificado!
        """
