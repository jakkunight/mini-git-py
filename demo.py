import os
import sys
import time
from pathlib import Path

# Agregar el directorio src al path
directorio_actual = Path(__file__).parent
directorio_src = directorio_actual / "src"
sys.path.insert(0, str(directorio_src))

from mini_git_py.ui.interfaz_usuario import InterfazUsuario


def imprimir_separador(titulo: str):

    print("\n" + "=" * 60)
    print(f"- {titulo}")
    print("=" * 60)


def pausa_demostración(segundos: int = 2):

    time.sleep(segundos)


def crear_archivos_ejemplo():

    archivos_ejemplo = {
        "saludo.txt": "¡Hola mundo desde Mini Git Python!",
        "programa.py": '''#!/usr/bin/env python3
"""
Programa de ejemplo para demostrar Mini Git Python
"""

def saludar(nombre):
    return f"¡Hola, {nombre}!"

if __name__ == "__main__":
    print(saludar("Usuario"))
''',
        "README.md": '''# Proyecto de Ejemplo

Este es un proyecto de demostración para **Mini Git Python**.

## Características

- Sistema de control de versiones simplificado
- Interfaz de línea de comandos intuitiva
- Manejo de objetos Git (blobs, trees, commits)

## Uso

```bash
python mini-git-py.py init
python mini-git-py.py add .
python mini-git-py.py commit -m "Primer commit"
```
''',
        "notas.txt": """Notas del proyecto:
- Implementar funcionalidad de branches
- Agregar soporte para merge
- Mejorar manejo de conflictos
- Documentar API interna
"""
    }
    
    print("Creando archivos de ejemplo...")
    for nombre_archivo, contenido in archivos_ejemplo.items():
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        print(f"   * {nombre_archivo}")
    
    return list(archivos_ejemplo.keys())


def demostrar_funcionalidades():

    print("DEMOSTRACIÓN DE MINI GIT PYTHON")
    print("Este script mostrará todas las funcionalidades del sistema")
    
    # Crear interfaz
    interfaz = InterfazUsuario()
    
    # 1. Inicializar repositorio
    imprimir_separador("PASO 1: Inicializar Repositorio")
    interfaz.ejecutar_desde_linea_comandos(['init'])
    pausa_demostración()
    
    # 2. Crear archivos de ejemplo
    imprimir_separador("PASO 2: Crear Archivos de Ejemplo")
    archivos_creados = crear_archivos_ejemplo()
    pausa_demostración()
    
    # 3. Ver estado inicial
    imprimir_separador("PASO 3: Ver Estado Inicial")
    interfaz.ejecutar_desde_linea_comandos(['status'])
    pausa_demostración()
    
    # 4. Agregar archivos
    imprimir_separador("PASO 4: Agregar Archivos al Área de Preparación")
    interfaz.ejecutar_desde_linea_comandos(['add', '.'])
    pausa_demostración()
    
    # 5. Ver estado después de add
    imprimir_separador("PASO 5: Ver Estado Después de Add")
    interfaz.ejecutar_desde_linea_comandos(['status'])
    pausa_demostración()
    
    # 6. Crear primer commit
    imprimir_separador("PASO 6: Crear Primer Commit")
    interfaz.ejecutar_desde_linea_comandos([
        'commit', 
        '-m', 'Commit inicial con archivos de ejemplo',
        '--autor-nombre', 'Demo Usuario',
        '--autor-email', 'demo@minigit.com'
    ])
    pausa_demostración()
    
    # 7. Ver historial
    imprimir_separador("PASO 7: Ver Historial de Commits")
    interfaz.ejecutar_desde_linea_comandos(['log'])
    pausa_demostración()
    
    # 8. Crear un blob específico
    imprimir_separador("PASO 8: Crear Blob de Archivo Específico")
    interfaz.ejecutar_desde_linea_comandos(['crear-blob', 'saludo.txt'])
    pausa_demostración()
    
    # 9. Crear tree
    imprimir_separador("PASO 9: Crear Tree del Directorio")
    interfaz.ejecutar_desde_linea_comandos(['crear-tree'])
    pausa_demostración()
    
    # 10. Modificar archivo y hacer segundo commit
    imprimir_separador("PASO 10: Modificar Archivo y Segundo Commit")
    with open('saludo.txt', 'a', encoding='utf-8') as archivo:
        archivo.write('\n\n¡Actualización desde la demostración!')
    
    print("Archivo saludo.txt modificado")
    interfaz.ejecutar_desde_linea_comandos(['add', 'saludo.txt'])
    interfaz.ejecutar_desde_linea_comandos([
        'commit',
        '-m', 'Actualizado archivo de saludo',
        '--autor-nombre', 'Demo Usuario',
        '--autor-email', 'demo@minigit.com'
    ])
    pausa_demostración()
    
    # 11. Ver historial final
    imprimir_separador("PASO 11: Historial Final de Commits")
    interfaz.ejecutar_desde_linea_comandos(['log'])
    pausa_demostración()
    
    # 12. Estado final
    imprimir_separador("PASO 12: Estado Final del Repositorio")
    interfaz.ejecutar_desde_linea_comandos(['status'])
    
    # Finalización
    imprimir_separador("DEMOSTRACIÓN COMPLETADA")
    print("¡Demostración exitosa de Mini Git Python!")
    print("\nFuncionalidades demostradas:")
    print("   * Inicialización de repositorio")
    print("   * Agregar archivos al área de preparación")
    print("   * Crear commits con mensajes y autores")
    print("   * Ver estado del repositorio")
    print("   * Ver historial de commits")
    print("   * Crear objetos blob y tree")
    print("   * Manejo de modificaciones de archivos")
    
    print("\nAhora puedes:")
    print("   * Explorar el directorio .mini-git para ver la estructura interna")
    print("   * Consultar GUIA_USO.md para más información")
    print("   * Usar configurar.py para establecer autor predeterminado")
    print("   * Experimentar con más comandos por tu cuenta")


def limpiar_archivos_demo():

    archivos_a_eliminar = [
        'saludo.txt', 'programa.py', 'README.md', 'notas.txt'
    ]
    
    directorios_a_eliminar = ['.mini-git']
    
    print("\n¿Quieres limpiar los archivos de demostración? (s/n): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("Limpiando archivos de demostración...")
        
        # Eliminar archivos
        for archivo in archivos_a_eliminar:
            if Path(archivo).exists():
                os.remove(archivo)
                print(f"   - {archivo}")
        
        # Eliminar directorios
        import shutil
        for directorio in directorios_a_eliminar:
            if Path(directorio).exists():
                shutil.rmtree(directorio)
                print(f"   - {directorio}/")
        
        print("Limpieza completada")
    else:
        print("Los archivos de demostración se mantienen para exploración")


def main():

    try:
        demostrar_funcionalidades()
        limpiar_archivos_demo()
    
    except KeyboardInterrupt:
        print("\n\nDemostración cancelada por el usuario")
    
    except Exception as error:
        print(f"\nError en la demostración: {error}")
        print("Verifica que todos los archivos estén en su lugar")


if __name__ == "__main__":
    main()