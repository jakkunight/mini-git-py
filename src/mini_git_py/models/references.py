class CommitReference:
    def __init__(self, name: str, commit_hash: str):
        if commit_hash == "":
            raise TypeError("El hash provisto no puede estar vacío.")

        if name == "":
            raise TypeError("El nombre de la referencia no puede ser nulo.")

        self.commit_hash = commit_hash
        self.name = name
