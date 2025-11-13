from dataclasses import dataclass


@dataclass
class Blob:
    content: str

    def __post_init__(self):
        pass

    def get_lines(self) -> list[str]:
        """Divide el contenido en líneas para el diff"""
        return self.content.splitlines(keepends=True)
