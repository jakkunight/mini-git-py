from dataclasses import dataclass
from hashlib import sha256


@dataclass
class GitObject:
    sha: str
    type: str
    size: int
    content: bytes

    def __post_init__(self):
        assert (
            self.type == "blob"
            or self.type == "tree"
            or self.type == "commit"
            or self.type == "tag"
        ), f"""
            El tipo de objeto ingresado debe ser:
            - "blob"
            - "tree"
            - "commit"
            - "tag"

            El valor provisto fue:
            - {self.type}
        """
        assert self.size == len(self.content), f"""
            El tamaño del contenido provisto no coincide con el tamaño real del contenido.

            Tamaño provisto:
            - {self.size}B

            Tamaño real:
            - {len(self.content)}B
        """

        separator: str = "\n\r"
        header: str = f"type {self.type}{separator}size {self.size}"
        final_content: str = f"{header}{separator}{self.content}"
        calculated_sha: str = sha256(final_content.encode("utf-8")).hexdigest()
        assert self.sha == calculated_sha, f"""
            El contenido o el hash provisto no corresponden entre sí.

            Hash provisto:
            - {self.sha}

            Hash real del contenido:
            - {calculated_sha}
        """
