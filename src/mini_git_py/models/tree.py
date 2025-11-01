from dataclasses import dataclass


@dataclass
class Tree:
    name: str
    type = "tree"

    def __post_init__(self):
        assert self.name != "", """
            El nombre provisto no puede ser vacío.
        """
