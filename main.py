# # Mini Git PY
# Un clon de Git, hecho con Python.

import sys
import os
from treelib import Tree
import hashlib
from abc import (
    ABC,
    ABCMeta,
    abstractmethod,
)

# # Qué es el Object-Database de Git?
#
# Es una tabla hash que guarda objetos de diversos tipos.
# Cada hash se genera a partir del contenido a guardar.
# Por ejemplo:
# ```python
# object_database = {} # Esto crea el diccionario.
# content = "Cambio de un archivo"
# hash = hasher(content)
# object_database[hash] = content
# ```
#
# # Qué se guarda en el Object-Database de Git?
#
# - Blobs: Representan el contenido de un archivo, sin
#   ningún tipo de metadatos.
# - Árboles: Representan las carpetas monitoreadaas por Git.
#   Sus hojas contienen referencias a otros árboles y blobs.
# - Commits: Un commit asocia un mensaje, un autor y una fecha
#   con un árbol, que representa el estado actual del proyecto.
#   Suele tener también una referencia al commit anterior.
# - Las ramas son simplemente referencias a commits específicos,
#   de modo a no tener que usar sus hashes para poder referirnos
#   a los mismos. Todo proyecto inicia con una rama 'master' o 'main'.
