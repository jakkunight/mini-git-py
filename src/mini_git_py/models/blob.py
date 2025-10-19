from hashlib import sha256


class Blob:
    """
    Una clase que representa el contenido de un archivo sin ningún metadato.
    """

    def __init__(self, file_content: str):
        self.content = file_content
        content_bytes = file_content.encode()
        raw_hash = sha256(content_bytes)
        hexadecimal_hash_string = raw_hash.hexdigest()
        self.hash = hexadecimal_hash_string
