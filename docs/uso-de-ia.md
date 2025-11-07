# Uso de la IA en el trabajo

## Técnica de generación de código con IA: Contexto de Modelado de Datos

> Esta técnica fue tomada del youtuber
> [@hdeleon.net](https://www.youtube.com/watch?v=V2iLgKDnXXU) en el video
> titulado: 'La Nueva Forma de Programar (Arquitectura + IA)'
>
> También se ha optado por un diseño más robusto basado en la convención de Go
> ['nil as error'](https://medium.com/@kotanetes/the-importance-of-passing-nil-to-error-channels-in-go-routines-ae3e8b91751f),
> y principalmente las ideas de
> [@CodeAesthetic](https://www.youtube.com/@CodeAesthetic) sobre arquitectura de
> software.

La técnica utilizada consta del siguiente proceso:

1. Crear **tipos de datos**, **clases**, e **interfaces** que definan las
   **reglas del negocio**.
2. Debido a que las excepciones no son del todo obligatorias de manejarse en
   Python, se usa la convención 'nil-as-error' para forzar al que llama a la
   función a manejar el 'error', representado como `None` en este caso.
3. Una vez definido el modelo, se pide a algún modelo de IA (ChatGPT, Gemini,
   Claude, DeepSeek, etc) que realice una implementación de las interfaces,
   respetando los tipos de datos definidos. De esta forma, se puede generar
   código rápido y muy sólido, pues el propio tipado de datos imposibilita la
   aparición de código incorrecto.
4. Luego se procede al análisis estático del código y su revisión. Si son
   necesarias, se realizan ajustes, bien utilizando IA, o manualmente.
5. Realizar los tests de integración y unitarios para garantizar el buen
   funcionamiento del proyecto.

## Sobre la documentación y los comentarios

Como señala @CodeAesthetic, es mucho mejor escribir _código legible y buena
documentación_, que _código ilegible y comentarios que intenten explicarlo_. En
este caso, se intenta que el código sea lo más legible y claro posible para el
desarrollador. Se ha optado por el uso de Docstrings en lugar de comentarios
para explicar **que hace** el código, en lugar del **como hace** las cosas el
código. En general, la IA genera código, en principio, más limpio que el de una
persona, por tanto también la usamos para "limpiar" código.
