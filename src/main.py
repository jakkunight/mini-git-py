import sys
from pathlib import Path

# Agregar el directorio src al path para importar módulos
directorio_actual = Path(__file__).parent
directorio_src = directorio_actual
sys.path.insert(0, str(directorio_src))

from mini_git_py.ui.interfaz_usuario import InterfazUsuario


def main():

    try:
        # Crear instancia de la interfaz de usuario
        interfaz = InterfazUsuario()
        
        # Ejecutar con argumentos de línea de comandos
        interfaz.ejecutar_desde_linea_comandos()
    
    except KeyboardInterrupt:
        # El usuario presionó Ctrl+C
        print("\n\nOperación cancelada por el usuario")
        sys.exit(1)
    
    except Exception as error:
        # Error inesperado
        print(f"\nError crítico: {error}")
        print("Si el problema persiste, reporta este error a los desarrolladores")
        sys.exit(1)


if __name__ == "__main__":
    main()
