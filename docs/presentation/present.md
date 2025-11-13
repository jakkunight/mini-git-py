---
title: "Magnesium: Un 'clon' de Git"
authors:
  - "Christian Álvarez"
  - "Eric Gonzáles"
  - "Raúl Ramírez"
  - "Santiago Wu"
  - "Lucas Zaracho"
---

<!-- deno-fmt-ignore -->
Devs en los 90's
================

Durante la década de los 90, el trabajo de los desarrolladores era muy diferente
al que conocemos hoy. La colaboración en proyectos de software era mucho más
complicada, y muchos de los problemas que hoy resolvemos con Git simplemente no
tenían solución estándar.

<!--deno-fmt-ignore-->
Colaboración limitada
========================

- Los equipos trabajaban de forma presencial, compartiendo el código en:

- Disquetes

- Carpetas en servidores locales

- E-mails con archivos adjuntos

- Copias llamadas “final”, “final2”, “finalahoraSi”

Todo esto generaba conflictos constantes y pérdida de versiones.

<!-- deno-fmt-ignore -->
Control de versiones “manual”
================================

Antes de que existieran herramientas modernas, los devs usaban métodos como:

- Copiar y renombrar carpetas (“Proyecto_v1”, “v1_copia”, “v1_BUENO”, etc.)

- Guardar archivos con fecha en el nombre

- Comentarios en el código diciendo “no tocar esta parte”

Era fácil romper algo y no poder volver atrás.

<!-- deno-fmt-ignore -->
Nacimiento de los primeros sistemas de control de versiones
==============================================================

A finales de los 80 y durante los 90 aparecieron los primeros intentos serios de
manejar versiones:

- RCS (Revision Control System) — Funcionaba por archivo, no por proyecto.

- CVS (Concurrent Versions System) — Permitía colaboración, pero dependía
  fuertemente de RCS.

- Más tarde, Subversion (SVN) vino a corregir muchas limitaciones.

Estas herramientas introdujeron conceptos que hoy damos por sentado: commits,
historial, repositorio, archivos versionados…

<!-- deno-fmt-ignore -->
Sistemas de Control de Versiones
================================

En el desarrollo de software, uno de los mayores desafíos es mantener un control
organizado sobre los cambios que se realizan a lo largo del tiempo.

Los sistemas de control de versiones (VCS) permiten registrar cada modificación
en un proyecto, restaurar versiones anteriores y trabajar de forma colaborativa
sin perder el historial de los cambios realizados.

<!-- deno-fmt-ignore -->
Git
===

Es un sistema muy poderoso y complejo, utilizado en prácticamente todos los
proyectos de software del mundo. Pero dentro de esa complejidad, hay una lógica
interna basada en estructuras de datos: los blobs, los árboles (trees), los
commits y las referencias.

<!-- deno-fmt-ignore -->
Arquitectura
============

<!-- deno-fmt-ignore -->
Tipos de Datos
==============

<!-- deno-fmt-ignore -->
Interfaces
==========

<!-- end_slide -->
<!-- jump_to_middle -->
<!-- text_align: center -->
<!-- deno-fmt-ignore -->
Demostración
============
