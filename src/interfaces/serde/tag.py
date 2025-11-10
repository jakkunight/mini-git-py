from abc import ABC, abstractmethod

from models.tag import Tag


class TagSerializer(ABC):
    @abstractmethod
    def serialize_tag(self, tag: Tag) -> str | None:
        pass

    @abstractmethod
    def deserialize_tag(self, data: str) -> Tag | None:
        pass
