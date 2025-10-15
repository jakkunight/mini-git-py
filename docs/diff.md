# Algoritmo para detectar los cambios en un archivo:

Una línea está...

- Eliminada: Si no existe en el commit actual, pero existe en el commit padre.
- Añadida: Si existe en el commit actual, pero no existe en el commit padre.
- Sin cambios: Si existe en ambos commits y en la misma posición.

```python
prev_lines = prev_blob.split("\r\n")
curr_lines = curr_blob.split("\r\n")

class LineDiff:
  def __init__(self, position, content, status = 0):
    # Line number:
    self.position = position

    # Line content:
    self.content = content
    
    # Status:
    #   Deleted = -1
    # Unchanged = 0
    #     Added = 1
    self.status = status

diffs = []
i = 0
while (!(i >= len(prev_lines) or i >= len(curr_lines))):
  
  i++
```
