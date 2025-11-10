import gzip
from typing import override
from interfaces.data_compressor import DataCompressor


class GzipCompressor(DataCompressor):
    @override
    def compress(self, data: bytes) -> bytes | None:
        return gzip.compress(data)

    @override
    def decompress(self, data: bytes) -> bytes | None:
        return gzip.decompress(data)
