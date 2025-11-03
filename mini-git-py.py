import sys
from pathlib import Path

# Obtener el directorio donde está este script
directorio_script = Path(__file__).parent.absolute()
directorio_src = directorio_script / "src"

# Agregar el directorio src al path de Python
sys.path.insert(0, str(directorio_src))

# Importar y ejecutar el programa principal
try:
    from main import main
    main()
except ImportError as error:
    print(f"Error al importar módulos: {error}")
    print(f"Verifica que el archivo está en: {directorio_src}")
    sys.exit(1)