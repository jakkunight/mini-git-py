---
title: "Magnesium: Un 'clon' de Git"
authors:
  - "Christian Alvarez"
  - "Eric Gonzáles"
  - "Raúl Ramírez"
  - "Santiago Wu"
  - "Lucas Zaracho"
---

<!-- deno-fmt-ignore -->
Devs en los 90's
================
 Durante la década de los 90, el trabajo de los desarrolladores era muy diferente al que conocemos hoy. La colaboración en proyectos de software era mucho más complicada, y muchos de los problemas que hoy resolvemos con Git simplemente no tenían solución estándar.

1. ## Colaboración limitada

-Los equipos trabajaban de forma presencial, compartiendo el código en:

-Disquetes

-Carpetas en servidores locales

-E-mails con archivos adjuntos

-Copias llamadas “final”, “final2”, “finalahoraSi”

Todo esto generaba conflictos constantes y pérdida de versiones.

2. ## Control de versiones “manual”

Antes de que existieran herramientas modernas, los devs usaban métodos como:

-Copiar y renombrar carpetas (“Proyecto_v1”, “v1_copia”, “v1_BUENO”, etc.)

-Guardar archivos con fecha en el nombre

-Comentarios en el código diciendo “no tocar esta parte”

Era fácil romper algo y no poder volver atrás.

3. ## Nacimiento de los primeros sistemas de control de versiones

A finales de los 80 y durante los 90 aparecieron los primeros intentos serios de manejar versiones:

-RCS (Revision Control System) — Funcionaba por archivo, no por proyecto.

-CVS (Concurrent Versions System) — Permitía colaboración, pero dependía fuertemente de RCS.

-Más tarde, Subversion (SVN) vino a corregir muchas limitaciones.

Estas herramientas introdujeron conceptos que hoy damos por sentado: commits, historial, repositorio, archivos versionados…


<!-- deno-fmt-ignore -->
# Sistemas de Control de Versiones
En el desarrollo de software, uno de los mayores desafíos es mantener un control organizado sobre los cambios que se realizan a lo largo del tiempo.

Los sistemas de control de versiones (VCS) permiten registrar cada modificación en un proyecto, restaurar versiones anteriores y trabajar de forma colaborativa sin perder el historial de los cambios realizados.

# Git
Es un sistema muy poderoso y complejo, utilizado en prácticamente todos los proyectos de software del mundo. Pero dentro de esa complejidad, hay una lógica interna basada en estructuras de datos: los blobs, los árboles (trees), los commits y las referencias.


<!-- deno-fmt-ignore -->

# MiniGit
MiniGit busca replicar la lógica central de GIT, permitiendo que podamos entender cómo un sistema de control de versiones almacena, organiza y recupera los cambios de un proyecto.


<!-- deno-fmt-ignore -->
# Objetivo general
 -	Desarrollar e implementar un sistema de control de versiones simplificado, denominado MiniGit.
# Objetivos Específicos
- Simular el funcionamiento de un sistema de control de versiones real.
- Diseñar y aplicar estructuras de datos eficientes.
- Comprender el flujo del versionado.
- Separar la lógica del sistema de control de versiones.
- Analizar la importancia del versionado.
- Demostrar la aplicación práctica de las estructuras de datos.
============

<!-- deno-fmt-ignore -->
# Importancia
El desarrollo de un sistema como MiniGit tiene una gran relevancia en el ámbito de la Ingeniería en Informática, ya que permite comprender de forma práctica los fundamentos del control de versiones, una de las herramientas más esenciales en el ciclo de vida del software.
A través de MiniGit, los estudiantes y profesionales podemos:
- Registro, almacenamiento y administracion de cambios.
- Análisis, diseño e implementación de estructuras de datos.
- Visión técnica y crítica.
============

<!-- deno-fmt-ignore -->
Arquitectura
============

<!-- deno-fmt-ignore -->
Tipos de Datos
==============

<!-- deno-fmt-ignore -->
Interfaces
==========

<!-- deno-fmt-ignore -->
Demostración
============
