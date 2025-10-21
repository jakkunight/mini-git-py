# Documentación sobre el funcionamiento de Git

## ¿Qué es el Object-Database de Git?

Es una tabla hash que guarda objetos de diversos tipos. Cada hash se genera a
partir del contenido a guardar. Por ejemplo:

```python
object_database = {} # Esto crea el diccionario.
content = "Cambio de un archivo"
hash = hasher(content)
object_database[hash] = content
```

## ¿Qué se guarda en el Object-Database de Git?

- Blobs: Representan el contenido de un archivo, sin ningún tipo de metadatos.
- Árboles: Representan las carpetas monitoreadaas por Git. Sus hojas contienen
  referencias a otros árboles y blobs.
- Commits: Un commit asocia un mensaje, un autor y una fecha con un árbol, que
  representa el estado actual del proyecto. Suele tener también una referencia
  al commit anterior.
- Las ramas son simplemente referencias a commits específicos, de modo a no
  tener que usar sus hashes para poder referirnos a los mismos. Todo proyecto
  inicia con una rama 'master' o 'main'.

<!-- deno-fmt-ignore -->
> [!note] Referencia del 1er commit
> En el campo de referencia al commit padre
> del 1er commit, se coloca un `00000000000000000000000000000000000000000`, que
> corresponde al directorio 'vacío'.

## Sobre el merging

Para hacer un merge, git usa 3 commits.

- Un commit base, común a los commits que se quieren fusionar.
- Un dos commits, que representan ramas divergentes.

## Sobre Git y los Grafos acíclicos

> Esta idea fue tomada de
> [@Antonio Sarosi](https://youtu.be/LjwR--_ZUt8?t=521&si=YESM8xDNDr7M-pI3)
> Muchas gracias por difundir este contenido en español.

Podemos imaginar el _object-database_ como un **grafo acíclico**, esto es, un
grafo en el que dado un punto de partida cualquiera, es imposible volver al
punto inicial siguiendo los caminos en el grafo.

Si vemos los **commits**, podemos ver la siguiente relación:

```mermaid
("commit 1") --> ["tree 1"]
("commit 1") --> ("commit 0")
```

O sea que, un **commit** cuenta con un camino hacia un tree, y otro hacia el
commit padre. Si este último camino **no existe**, entonces estamos ante el
**primer commit del repositorio**.

Un **tree**, o árbol, es en sí mismo una lista de punteros a dos tipos de nodos:
los **blobs** y **otros trees**.

```mermaid
["tree 1"] --> ["tree 2"]
["tree 1"] --> {"blob 1"}
["tree 2"] --> {"blob 2"}
["tree 2"] --> {"blob 3"}
```

Como se puede apreciar, **todo camino termina en un blob**.
