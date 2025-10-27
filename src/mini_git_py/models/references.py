class CommitReference:
    def __init__(self, commit_hash: str):
        if commit_hash == "":
            raise TypeError("El hash provisto no puede estar vacío.")

        self.commit_hash = commit_hash
