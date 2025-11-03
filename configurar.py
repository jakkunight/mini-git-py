import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Agregar el directorio src al path
directorio_actual = Path(__file__).parent
directorio_src = directorio_actual / "src"
sys.path.insert(0, str(directorio_src))

from mini_git_py.ui.comandos_usuario import ComandosUsuario, ResultadoComando


class ConfiguradorMiniGit:

    def __init__(self):
        self.directorio_trabajo = Path.cwd()
        self.directorio_git = self.directorio_trabajo / ".mini-git"
        self.archivo_configuracion = self.directorio_git / "config.json"
    
    def configurar_autor_predeterminado(self, nombre: str, email: str) -> ResultadoComando:
    
        try:
            if not self.directorio_git.exists():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado. Ejecuta 'init' primero."
                )
            
            # Cargar configuración actual
            configuracion = self._cargar_configuracion()
            
            # Actualizar información del autor
            configuracion["autor_predeterminado"] = {
                "nombre": nombre,
                "email": email
            }
            
            # Guardar configuración
            self._guardar_configuracion(configuracion)
            
            return ResultadoComando(
                True,
                "Autor predeterminado configurado exitosamente",
                {"nombre": nombre, "email": email}
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al configurar autor: {error}"
            )
    
    def obtener_configuracion_actual(self) -> ResultadoComando:

        try:
            if not self.directorio_git.exists():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado"
                )
            
            configuracion = self._cargar_configuracion()
            
            return ResultadoComando(
                True,
                "Configuración obtenida exitosamente",
                configuracion
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al obtener configuración: {error}"
            )
    
    def mostrar_configuracion(self) -> None:

        resultado = self.obtener_configuracion_actual()
        
        if not resultado.fue_exitoso:
            print(f"Error: {resultado.mensaje}")
            return
        
        config = resultado.datos
        
        print("CONFIGURACIÓN ACTUAL DE MINI GIT:")
        print("=" * 45)
        print(f"Versión: {config.get('version', 'Desconocida')}")
        print(f"Rama actual: {config.get('rama_actual', 'master')}")
        
        autor = config.get('autor_predeterminado', {})
        if autor.get('nombre') and autor.get('email'):
            print(f"Autor predeterminado: {autor['nombre']} <{autor['email']}>")
        else:
            print("Autor predeterminado: No configurado")
        
        print(f"Repositorio inicializado: {'Sí' if config.get('repositorio_inicializado') else 'No'}")
    
    def _cargar_configuracion(self) -> Dict[str, Any]:

        with open(self.archivo_configuracion, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    
    def _guardar_configuracion(self, configuracion: Dict[str, Any]) -> None:

        with open(self.archivo_configuracion, 'w', encoding='utf-8') as archivo:
            json.dump(configuracion, archivo, indent=2, ensure_ascii=False)


def main():

    print("CONFIGURADOR DE MINI GIT PYTHON")
    print("=" * 40)
    
    configurador = ConfiguradorMiniGit()
    
    # Mostrar configuración actual
    configurador.mostrar_configuracion()
    
    print("\n" + "=" * 40)
    print("CONFIGURAR AUTOR PREDETERMINADO")
    
    try:
        # Solicitar información del usuario
        nombre = input("\nIngresa tu nombre: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return
        
        email = input("Ingresa tu email: ").strip()
        if not email:
            print("Error: El email no puede estar vacío")
            return
        
        # Configurar autor
        resultado = configurador.configurar_autor_predeterminado(nombre, email)
        
        if resultado.fue_exitoso:
            print(f"\nAutor configurado exitosamente:")
            print(f"   Nombre: {nombre}")
            print(f"   Email: {email}")
            print("\nAhora puedes hacer commits sin especificar --autor-nombre y --autor-email")
        else:
            print(f"\nError: {resultado.mensaje}")
    
    except KeyboardInterrupt:
        print("\n\nConfiguración cancelada por el usuario")
    
    except Exception as error:
        print(f"\nError inesperado: {error}")


if __name__ == "__main__":
    main()