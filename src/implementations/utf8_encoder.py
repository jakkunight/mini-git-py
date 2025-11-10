from typing import override
from interfaces.data_encoder import DataEncoder


class Utf8Encoder(DataEncoder):
    @override
    def encode(self, data: str) -> bytes:
        return data.encode("utf-8")

    @override
    def decode(self, data: bytes) -> str:
        return data.decode("utf-8")
