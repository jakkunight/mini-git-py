import sys
import argparse
from typing import List, Optional
from mini_git_py.ui.comandos_usuario import ComandosUsuario
from mini_git_py.ui.ayuda_usuario import AyudaUsuario


class InterfazUsuario:
    
    def __init__(self):
        self.comandos_usuario = ComandosUsuario()
        self.ayuda_usuario = AyudaUsuario()
        self.parser_argumentos = self._configurar_parser_argumentos()
    
    def _configurar_parser_argumentos(self) -> argparse.ArgumentParser:
        
        parser = argparse.ArgumentParser(
            prog='mini-git-py',
            description='Sistema de control de versiones Mini Git en Python',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self.ayuda_usuario.obtener_ejemplos_uso()
        )
        
        # Crear subparsers para los diferentes comandos
        subparsers = parser.add_subparsers(
            dest='comando',
            help='Comandos disponibles en Mini Git'
        )
        
        # Comando: init (inicializar repositorio)
        parser_init = subparsers.add_parser(
            'init',
            help='Inicializar un nuevo repositorio Mini Git'
        )
        
        # Comando: add (agregar archivos)
        parser_add = subparsers.add_parser(
            'add',
            help='Agregar archivos al área de preparación (staging)'
        )
        parser_add.add_argument(
            'archivos',
            nargs='+',
            help='Archivos a agregar (usa "." para todos los archivos)'
        )
        
        # Comando: commit (crear commit)
        parser_commit = subparsers.add_parser(
            'commit',
            help='Crear un nuevo commit con los cambios preparados'
        )
        parser_commit.add_argument(
            '-m', '--mensaje',
            required=True,
            help='Mensaje descriptivo del commit'
        )
        parser_commit.add_argument(
            '--autor-nombre',
            help='Nombre del autor del commit'
        )
        parser_commit.add_argument(
            '--autor-email',
            help='Email del autor del commit'
        )
        
        # Comando: status (ver estado)
        parser_status = subparsers.add_parser(
            'status',
            help='Mostrar el estado actual del repositorio'
        )
        
        # Comando: log (ver historial)
        parser_log = subparsers.add_parser(
            'log',
            help='Mostrar el historial de commits'
        )
        parser_log.add_argument(
            '--cantidad',
            type=int,
            default=10,
            help='Número de commits a mostrar (por defecto: 10)'
        )
        
        # Comando: crear-blob
        parser_blob = subparsers.add_parser(
            'crear-blob',
            help='Crear un objeto blob con contenido específico'
        )
        parser_blob.add_argument(
            'archivo',
            help='Archivo del cual crear el blob'
        )
        
        # Comando: crear-tree
        parser_tree = subparsers.add_parser(
            'crear-tree',
            help='Crear un objeto tree del directorio actual'
        )
        
        # Comando: mostrar-objeto
        parser_show = subparsers.add_parser(
            'mostrar-objeto',
            help='Mostrar el contenido de un objeto Git'
        )
        parser_show.add_argument(
            'hash_objeto',
            help='Hash del objeto a mostrar'
        )
        
        return parser
    
    def ejecutar_desde_linea_comandos(self, argumentos: Optional[List[str]] = None) -> None:

        if argumentos is None:
            argumentos = sys.argv[1:]
        
        # Si no hay argumentos, mostrar ayuda
        if not argumentos:
            self.parser_argumentos.print_help()
            return
        
        try:
            args = self.parser_argumentos.parse_args(argumentos)
            self._ejecutar_comando(args)
        except SystemExit:
            # argparse llama a SystemExit cuando hay errores
            pass
        except Exception as error:
            self._mostrar_error(f"Error inesperado: {error}")
    
    def _ejecutar_comando(self, args) -> None:

        try:
            if args.comando == 'init':
                self._ejecutar_init()
            
            elif args.comando == 'add':
                self._ejecutar_add(args.archivos)
            
            elif args.comando == 'commit':
                self._ejecutar_commit(
                    args.mensaje,
                    args.autor_nombre,
                    args.autor_email
                )
            
            elif args.comando == 'status':
                self._ejecutar_status()
            
            elif args.comando == 'log':
                self._ejecutar_log(args.cantidad)
            
            elif args.comando == 'crear-blob':
                self._ejecutar_crear_blob(args.archivo)
            
            elif args.comando == 'crear-tree':
                self._ejecutar_crear_tree()
            
            elif args.comando == 'mostrar-objeto':
                self._ejecutar_mostrar_objeto(args.hash_objeto)
            
            else:
                self._mostrar_error("Comando no reconocido")
                self.parser_argumentos.print_help()
        
        except Exception as error:
            self._mostrar_error(f"Error al ejecutar comando '{args.comando}': {error}")
    
    def _ejecutar_init(self) -> None:

        resultado = self.comandos_usuario.inicializar_repositorio()
        if resultado.fue_exitoso:
            print(" Repositorio Mini Git inicializado correctamente")
            print(f" Ubicación: {resultado.mensaje}")
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_add(self, archivos: List[str]) -> None:

        resultado = self.comandos_usuario.agregar_archivos(archivos)
        if resultado.fue_exitoso:
            print(" Archivos agregados al área de preparación:")
            for archivo in resultado.datos.get('archivos_agregados', []):
                print(f" {archivo}")
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_commit(self, mensaje: str, autor_nombre: Optional[str], autor_email: Optional[str]) -> None:

        resultado = self.comandos_usuario.crear_commit(mensaje, autor_nombre, autor_email)
        if resultado.fue_exitoso:
            print(" Commit creado exitosamente")
            print(f" Hash: {resultado.datos.get('hash_commit')}")
            print(f" Mensaje: {mensaje}")
            print(f" Autor: {resultado.datos.get('autor_nombre')} <{resultado.datos.get('autor_email')}>")
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_status(self) -> None:

        resultado = self.comandos_usuario.obtener_estado_repositorio()
        if resultado.fue_exitoso:
            self._mostrar_estado_repositorio(resultado.datos)
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_log(self, cantidad: int) -> None:

        resultado = self.comandos_usuario.obtener_historial_commits(cantidad)
        if resultado.fue_exitoso:
            self._mostrar_historial_commits(resultado.datos.get('commits', []))
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_crear_blob(self, archivo: str) -> None:

        resultado = self.comandos_usuario.crear_blob_desde_archivo(archivo)
        if resultado.fue_exitoso:
            print(" Blob creado exitosamente")
            print(f" Hash: {resultado.datos.get('hash_blob')}")
            print(f" Archivo: {archivo}")
            print(f" Tamaño: {resultado.datos.get('tamaño_contenido')} bytes")
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_crear_tree(self) -> None:

        resultado = self.comandos_usuario.crear_tree_directorio_actual()
        if resultado.fue_exitoso:
            print(" Tree creado exitosamente")
            print(f" Hash: {resultado.datos.get('hash_tree')}")
            print(f" Entradas: {resultado.datos.get('cantidad_entradas')} elementos")
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _ejecutar_mostrar_objeto(self, hash_objeto: str) -> None:

        resultado = self.comandos_usuario.mostrar_contenido_objeto(hash_objeto)
        if resultado.fue_exitoso:
            print(f" Objeto: {hash_objeto}")
            print(f" Tipo: {resultado.datos.get('tipo_objeto')}")
            print(" Contenido:")
            print("-" * 50)
            print(resultado.datos.get('contenido_objeto'))
        else:
            self._mostrar_error(resultado.mensaje)
    
    def _mostrar_estado_repositorio(self, datos_estado: dict) -> None:

        print(" Estado del repositorio Mini Git:")
        print(f" Rama actual: {datos_estado.get('rama_actual', 'master')}")
        
        archivos_preparados = datos_estado.get('archivos_preparados', [])
        archivos_modificados = datos_estado.get('archivos_modificados', [])
        archivos_no_rastreados = datos_estado.get('archivos_no_rastreados', [])
        
        if archivos_preparados:
            print("\n Archivos preparados para commit:")
            for archivo in archivos_preparados:
                print(f" {archivo}")
        
        if archivos_modificados:
            print("\n Archivos modificados:")
            for archivo in archivos_modificados:
                print(f" {archivo}")
        
        if archivos_no_rastreados:
            print("\n Archivos no rastreados:")
            for archivo in archivos_no_rastreados:
                print(f" {archivo}")
        
        if not any([archivos_preparados, archivos_modificados, archivos_no_rastreados]):
            print("\n El directorio de trabajo está limpio")
    
    def _mostrar_historial_commits(self, commits: List[dict]) -> None:

        if not commits:
            print(" No hay commits en el historial")
            return
        
        print(" Historial de commits:")
        print("=" * 60)
        
        for i, commit in enumerate(commits):
            print(f"\n Commit {i + 1}:")
            print(f" Hash: {commit.get('hash')}")
            print(f" Autor: {commit.get('autor_nombre')} <{commit.get('autor_email')}>")
            print(f" Fecha: {commit.get('fecha')}")
            print(f" Mensaje: {commit.get('mensaje')}")
            
            if i < len(commits) - 1:
                print("-" * 40)
    
    def _mostrar_error(self, mensaje_error: str) -> None:

        print(f" Error: {mensaje_error}")
    
    def mostrar_ayuda_completa(self) -> None:

        self.ayuda_usuario.mostrar_ayuda_completa()