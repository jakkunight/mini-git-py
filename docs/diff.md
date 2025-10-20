# Algoritmo para detectar los cambios en un archivo:

Una línea está...

- Eliminada: Si no existe en el commit actual, pero existe en el commit padre.
- Añadida: Si existe en el commit actual, pero no existe en el commit padre.
- Sin cambios: Si existe en ambos commits y en la misma posición.
