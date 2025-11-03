from typing import List

class AyudaUsuario:

    def __init__(self):
        self.nombre_programa = "mini-git-py"
        self.version = "1.0.0"
    
    def obtener_ejemplos_uso(self) -> str:

        ejemplos = f"""
EJEMPLOS DE USO:

  Inicializar un repositorio:
    {self.nombre_programa} init

  Agregar archivos:
    {self.nombre_programa} add archivo.txt
    {self.nombre_programa} add archivo1.txt archivo2.txt
    {self.nombre_programa} add .  # Agregar todos los archivos

  Crear un commit:
    {self.nombre_programa} commit -m "Mi primer commit"
    {self.nombre_programa} commit -m "Agregado nueva funcionalidad" --autor-nombre "Juan Pérez" --autor-email "juan@email.com"

  Ver estado del repositorio:
    {self.nombre_programa} status

  Ver historial de commits:
    {self.nombre_programa} log
    {self.nombre_programa} log --cantidad 5  # Mostrar solo 5 commits

  Trabajar con objetos:
    {self.nombre_programa} crear-blob archivo.txt
    {self.nombre_programa} crear-tree
    {self.nombre_programa} mostrar-objeto a1b2c3d4e5f6...

Para más información sobre un comando específico:
    {self.nombre_programa} <comando> --help
        """
        return ejemplos.strip()
    
    def obtener_guia_rapida(self) -> str:

        guia = f"""
GUÍA RÁPIDA DE {self.nombre_programa.upper()}

COMANDOS BÁSICOS:
  init     - Inicializar repositorio
  add      - Agregar archivos al área de preparación
  commit   - Crear un commit con los cambios
  status   - Ver estado del repositorio
  log      - Ver historial de commits

COMANDOS AVANZADOS:
  crear-blob      - Crear objeto blob de un archivo
  crear-tree      - Crear objeto tree del directorio
  mostrar-objeto  - Mostrar contenido de un objeto

FLUJO TÍPICO:
  1. {self.nombre_programa} init
  2. {self.nombre_programa} add .
  3. {self.nombre_programa} commit -m "Primer commit"
  4. {self.nombre_programa} status
        """
        return guia.strip()
    
    def obtener_descripcion_comandos(self) -> dict:

        comandos = {
            "init": {
                "descripcion": "Inicializa un nuevo repositorio Mini Git",
                "uso": f"{self.nombre_programa} init",
                "detalles": [
                    "Crea la carpeta .mini-git con la estructura necesaria",
                    "Configura el repositorio para comenzar a trabajar",
                    "Solo necesita ejecutarse una vez por proyecto"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} init"
                ]
            },
            
            "add": {
                "descripcion": "Agrega archivos al área de preparación (staging)",
                "uso": f"{self.nombre_programa} add <archivos...>",
                "detalles": [
                    "Prepara archivos para ser incluidos en el próximo commit",
                    "Puede agregar uno o varios archivos a la vez",
                    "Use '.' para agregar todos los archivos del directorio"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} add archivo.txt",
                    f"{self.nombre_programa} add archivo1.txt archivo2.txt",
                    f"{self.nombre_programa} add ."
                ]
            },
            
            "commit": {
                "descripcion": "Crea un commit con los archivos preparados",
                "uso": f"{self.nombre_programa} commit -m \"mensaje\"",
                "detalles": [
                    "Guarda los cambios preparados como un nuevo commit",
                    "Requiere un mensaje descriptivo obligatorio",
                    "Puede especificar autor con --autor-nombre y --autor-email"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} commit -m \"Primer commit\"",
                    f"{self.nombre_programa} commit -m \"Nueva funcionalidad\" --autor-nombre \"Ana\" --autor-email \"ana@email.com\""
                ]
            },
            
            "status": {
                "descripcion": "Muestra el estado actual del repositorio",
                "uso": f"{self.nombre_programa} status",
                "detalles": [
                    "Muestra archivos preparados para commit",
                    "Lista archivos modificados pero no preparados",
                    "Indica archivos no rastreados por el sistema"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} status"
                ]
            },
            
            "log": {
                "descripcion": "Muestra el historial de commits",
                "uso": f"{self.nombre_programa} log [--cantidad N]",
                "detalles": [
                    "Lista los commits en orden cronológico",
                    "Muestra hash, autor, fecha y mensaje de cada commit",
                    "Puede limitar la cantidad de commits mostrados"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} log",
                    f"{self.nombre_programa} log --cantidad 5"
                ]
            },
            
            "crear-blob": {
                "descripcion": "Crea un objeto blob de un archivo específico",
                "uso": f"{self.nombre_programa} crear-blob <archivo>",
                "detalles": [
                    "Convierte el contenido de un archivo en un objeto blob",
                    "Calcula y muestra el hash SHA-256 del objeto",
                    "Almacena el objeto en la base de datos del repositorio"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} crear-blob archivo.txt"
                ]
            },
            
            "crear-tree": {
                "descripcion": "Crea un objeto tree del directorio actual",
                "uso": f"{self.nombre_programa} crear-tree",
                "detalles": [
                    "Genera un árbol que representa la estructura del directorio",
                    "Incluye referencias a archivos y subdirectorios",
                    "Fundamental para el sistema de objetos de Git"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} crear-tree"
                ]
            },
            
            "mostrar-objeto": {
                "descripcion": "Muestra el contenido de un objeto Git",
                "uso": f"{self.nombre_programa} mostrar-objeto <hash>",
                "detalles": [
                    "Permite inspeccionar el contenido de cualquier objeto",
                    "Muestra el tipo de objeto (blob, tree, commit)",
                    "Útil para debugging y comprensión del sistema"
                ],
                "ejemplos": [
                    f"{self.nombre_programa} mostrar-objeto a1b2c3d4e5f6789..."
                ]
            }
        }
        
        return comandos
    
    def mostrar_ayuda_completa(self) -> None:

        print(f"{self.nombre_programa.upper()} - Sistema de Control de Versiones")
        print(f"Versión: {self.version}")
        print("=" * 60)
        
        # Mostrar guía rápida
        print(self.obtener_guia_rapida())
        print("\n" + "=" * 60)
        
        # Mostrar descripción detallada de comandos
        print("\nDESCRIPCIÓN DETALLADA DE COMANDOS:\n")
        
        comandos = self.obtener_descripcion_comandos()
        for nombre_comando, info in comandos.items():
            print(f"{nombre_comando.upper()}")
            print(f"   Descripción: {info['descripcion']}")
            print(f"   Uso: {info['uso']}")
            
            print("   Detalles:")
            for detalle in info['detalles']:
                print(f"      • {detalle}")
            
            print("   Ejemplos:")
            for ejemplo in info['ejemplos']:
                print(f"      > {ejemplo}")
            
            print()  # Línea en blanco entre comandos
        
        # Mostrar ejemplos adicionales
        print("=" * 60)
        print(self.obtener_ejemplos_uso())
    
    def obtener_ayuda_comando(self, nombre_comando: str) -> str:

        comandos = self.obtener_descripcion_comandos()
        
        if nombre_comando not in comandos:
            return f"No se encontró ayuda para el comando '{nombre_comando}'"
        
        info = comandos[nombre_comando]
        
        ayuda = f"""
COMANDO: {nombre_comando.upper()}

Descripción:
   {info['descripcion']}

Uso:
   {info['uso']}

Detalles:"""
        
        for detalle in info['detalles']:
            ayuda += f"\n   • {detalle}"
        
        ayuda += "\n\nEjemplos:"
        
        for ejemplo in info['ejemplos']:
            ayuda += f"\n   > {ejemplo}"
        
        return ayuda.strip()
    
    def obtener_consejos_uso(self) -> List[str]:

        consejos = [
            "Usa mensajes de commit descriptivos para facilitar el seguimiento",
            "Ejecuta 'status' regularmente para conocer el estado de tu repositorio",
            "Organiza tus archivos antes de hacer 'add .' para evitar agregar archivos innecesarios",
            "Los nombres de archivos y mensajes con espacios deben ir entre comillas",
            "Puedes usar 'log --cantidad 1' para ver solo el último commit",
            "Configura un autor predeterminado para evitar especificarlo en cada commit",
            "El comando 'mostrar-objeto' es útil para entender cómo funciona Git internamente",
            "Experimenta con 'crear-blob' y 'crear-tree' para aprender sobre objetos Git",
            "El directorio '.mini-git' contiene toda la información del repositorio",
            "Puedes hacer múltiples 'add' antes de un 'commit' para preparar varios archivos"
        ]
        
        return consejos
    
    def mostrar_consejos_aleatorios(self, cantidad: int = 3) -> None:

        import random
        
        consejos = self.obtener_consejos_uso()
        consejos_seleccionados = random.sample(consejos, min(cantidad, len(consejos)))
        
        print("CONSEJOS ÚTILES:")
        for consejo in consejos_seleccionados:
            print(f"   {consejo}")
    
    def obtener_solucion_errores_comunes(self) -> dict:

        soluciones = {
            "repositorio_no_inicializado": {
                "error": "No hay un repositorio Mini Git inicializado",
                "solucion": f"Ejecuta '{self.nombre_programa} init' en el directorio donde quieres crear el repositorio",
                "ejemplo": f"{self.nombre_programa} init"
            },
            
            "archivo_no_existe": {
                "error": "El archivo especificado no existe",
                "solucion": "Verifica que el nombre del archivo sea correcto y que exista en el directorio actual",
                "ejemplo": "ls  # para ver archivos disponibles"
            },
            
            "sin_archivos_preparados": {
                "error": "No hay archivos preparados para hacer commit",
                "solucion": f"Usa '{self.nombre_programa} add' para preparar archivos antes de hacer commit",
                "ejemplo": f"{self.nombre_programa} add archivo.txt"
            },
            
            "autor_requerido": {
                "error": "Nombre o email del autor requerido",
                "solucion": "Especifica autor con --autor-nombre y --autor-email, o configura un autor predeterminado",
                "ejemplo": f"{self.nombre_programa} commit -m \"mensaje\" --autor-nombre \"Tu Nombre\" --autor-email \"tu@email.com\""
            },
            
            "objeto_no_encontrado": {
                "error": "El objeto con el hash especificado no existe",
                "solucion": "Verifica que el hash sea correcto. Puedes ver hashes disponibles con 'log'",
                "ejemplo": f"{self.nombre_programa} log"
            }
        }
        
        return soluciones
    
    def buscar_solucion_error(self, mensaje_error: str) -> str:

        soluciones = self.obtener_solucion_errores_comunes()
        
        # Búsqueda simple por palabras clave
        for clave, info in soluciones.items():
            if any(palabra in mensaje_error.lower() for palabra in info['error'].lower().split()):
                return f"""
POSIBLE SOLUCIÓN:

Error detectado: {info['error']}

Solución: {info['solucion']}

Ejemplo: {info['ejemplo']}
                """.strip()
        
        return "No se encontró una solución específica para este error. Consulta la documentación completa."