import gzip
# 1. Read blobs:
#   1. Commits:
#   2. Trees:
#   3. Blobs:


def commit_reader(commit_hash):
    commit_file = gzip.open(".mini-git-py/objects/" + commit_hash, "rb")
    decompressed_file = commit_file.read()
    commit_fields = decompressed_file.split("\n")
    commit = Commit()


# 2. Slice and compare lines:
# 3. Make the diff:
