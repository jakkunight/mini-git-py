from pathlib import Path
from typing import override
from interfaces.file_store import FileStore


class FileSystemStore(FileStore):
    def __init__(self) -> None:
        pass

    @override
    def load(self, path: Path) -> bytes | None:
        try:
            assert path.exists()
            file = open(path, "rb")
            result = file.read()

        except Exception as e:
            print(e)
            return None

        return result

    @override
    def save(self, path: Path, data: bytes) -> int | None:
        try:
            assert path.exists()
            file = open(path, "wb")
            result = file.write(data)
            assert result == len(data)

        except Exception as e:
            print(e)
            return None

        return result
