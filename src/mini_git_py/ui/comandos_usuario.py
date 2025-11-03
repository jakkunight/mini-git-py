import os
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from mini_git_py.models.author import Author
from mini_git_py.models.blob import Blob
from mini_git_py.models.tree import Tree, BlobEntry, TreeEntry
from mini_git_py.models.commit import Commit


class ResultadoComando:

    def __init__(self, fue_exitoso: bool, mensaje: str = "", datos: Optional[Dict[str, Any]] = None):
        self.fue_exitoso = fue_exitoso
        self.mensaje = mensaje
        self.datos = datos or {}


class ComandosUsuario:

    def __init__(self):
        self.directorio_trabajo = Path.cwd()
        self.directorio_git = self.directorio_trabajo / ".mini-git"
        self.archivo_configuracion = self.directorio_git / "config.json"
        self.directorio_objetos = self.directorio_git / "objects"
        self.archivo_indice = self.directorio_git / "index.json"
    
    def inicializar_repositorio(self) -> ResultadoComando:
  
        try:
            # Verificar si ya existe un repositorio
            if self.directorio_git.exists():
                return ResultadoComando(
                    False,
                    "Ya existe un repositorio Mini Git en este directorio"
                )
            
            # Crear estructura de directorios
            self.directorio_git.mkdir()
            self.directorio_objetos.mkdir()
            
            # Crear archivo de configuración inicial
            configuracion_inicial = {
                "version": "1.0",
                "repositorio_inicializado": True,
                "rama_actual": "master",
                "autor_predeterminado": {
                    "nombre": "",
                    "email": ""
                }
            }
            
            with open(self.archivo_configuracion, 'w', encoding='utf-8') as archivo:
                json.dump(configuracion_inicial, archivo, indent=2, ensure_ascii=False)
            
            # Crear archivo de índice vacío
            indice_inicial = {
                "archivos_preparados": {},
                "ultima_actualizacion": ""
            }
            
            with open(self.archivo_indice, 'w', encoding='utf-8') as archivo:
                json.dump(indice_inicial, archivo, indent=2, ensure_ascii=False)
            
            return ResultadoComando(
                True,
                str(self.directorio_git),
                {"directorio_git": str(self.directorio_git)}
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al inicializar repositorio: {error}"
            )
    
    def agregar_archivos(self, nombres_archivos: List[str]) -> ResultadoComando:

        try:
            if not self._verificar_repositorio_existe():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado en este directorio"
                )
            
            archivos_agregados = []
            
            # Cargar índice actual
            indice = self._cargar_indice()
            
            for nombre_archivo in nombres_archivos:
                if nombre_archivo == ".":
                    # Agregar todos los archivos del directorio actual
                    archivos_encontrados = self._obtener_todos_archivos()
                    for archivo in archivos_encontrados:
                        resultado_archivo = self._agregar_archivo_individual(archivo, indice)
                        if resultado_archivo:
                            archivos_agregados.append(archivo)
                else:
                    # Agregar archivo específico
                    archivo_path = self.directorio_trabajo / nombre_archivo
                    if archivo_path.exists() and archivo_path.is_file():
                        resultado_archivo = self._agregar_archivo_individual(nombre_archivo, indice)
                        if resultado_archivo:
                            archivos_agregados.append(nombre_archivo)
                    else:
                        return ResultadoComando(
                            False,
                            f"El archivo '{nombre_archivo}' no existe"
                        )
            
            # Guardar índice actualizado
            self._guardar_indice(indice)
            
            return ResultadoComando(
                True,
                f"Se agregaron {len(archivos_agregados)} archivo(s)",
                {"archivos_agregados": archivos_agregados}
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al agregar archivos: {error}"
            )
    
    def crear_commit(self, mensaje: str, nombre_autor: Optional[str] = None, email_autor: Optional[str] = None) -> ResultadoComando:

        try:
            if not self._verificar_repositorio_existe():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado en este directorio"
                )
            
            # Obtener información del autor
            info_autor = self._obtener_informacion_autor(nombre_autor, email_autor)
            if not info_autor["valido"]:
                return ResultadoComando(False, info_autor["error"])
            
            autor = Author(info_autor["nombre"], info_autor["email"])
            
            # Verificar que hay archivos preparados
            indice = self._cargar_indice()
            if not indice["archivos_preparados"]:
                return ResultadoComando(
                    False,
                    "No hay archivos preparados para hacer commit. Usa 'add' primero."
                )
            
            # Crear tree del estado actual
            resultado_tree = self._crear_tree_desde_indice(indice)
            if not resultado_tree["exitoso"]:
                return ResultadoComando(False, resultado_tree["error"])
            
            # Obtener hash del commit padre (si existe)
            hash_padre = self._obtener_ultimo_commit()
            
            # Crear commit
            commit = Commit(
                autor=autor,
                message=mensaje,
                tree_hash=resultado_tree["hash"],
                parent_hash=hash_padre or "0000000000000000000000000000000000000000"
            )
            
            # Guardar commit como objeto
            hash_commit = commit.compute_hash()
            ruta_objeto_commit = self.directorio_objetos / hash_commit
            
            with open(ruta_objeto_commit, 'w', encoding='utf-8') as archivo:
                archivo.write(commit.get_content())
            
            # Actualizar referencia HEAD
            self._actualizar_head(hash_commit)
            
            # Limpiar área de preparación
            indice["archivos_preparados"] = {}
            self._guardar_indice(indice)
            
            return ResultadoComando(
                True,
                "Commit creado exitosamente",
                {
                    "hash_commit": hash_commit,
                    "autor_nombre": autor.name,
                    "autor_email": autor.email,
                    "mensaje": mensaje
                }
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al crear commit: {error}"
            )
    
    def obtener_estado_repositorio(self) -> ResultadoComando:

        try:
            if not self._verificar_repositorio_existe():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado en este directorio"
                )
            
            configuracion = self._cargar_configuracion()
            indice = self._cargar_indice()
            
            # Obtener archivos en diferentes estados
            archivos_preparados = list(indice["archivos_preparados"].keys())
            archivos_directorio = self._obtener_todos_archivos()
            archivos_no_rastreados = [
                archivo for archivo in archivos_directorio
                if archivo not in indice["archivos_preparados"]
            ]
            
            # Por simplificación, no detectamos archivos modificados en esta versión
            archivos_modificados = []
            
            return ResultadoComando(
                True,
                "Estado obtenido exitosamente",
                {
                    "rama_actual": configuracion.get("rama_actual", "master"),
                    "archivos_preparados": archivos_preparados,
                    "archivos_modificados": archivos_modificados,
                    "archivos_no_rastreados": archivos_no_rastreados
                }
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al obtener estado: {error}"
            )
    
    def obtener_historial_commits(self, cantidad: int = 10) -> ResultadoComando:

        try:
            if not self._verificar_repositorio_existe():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado en este directorio"
                )
            
            commits = []
            hash_commit_actual = self._obtener_ultimo_commit()
            
            contador = 0
            while hash_commit_actual and contador < cantidad:
                commit_info = self._obtener_informacion_commit(hash_commit_actual)
                if commit_info:
                    commits.append(commit_info)
                    hash_commit_actual = commit_info.get("parent_hash")
                    if hash_commit_actual == "0000000000000000000000000000000000000000":
                        break
                    contador += 1
                else:
                    break
            
            return ResultadoComando(
                True,
                f"Se encontraron {len(commits)} commit(s)",
                {"commits": commits}
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al obtener historial: {error}"
            )
    
    def crear_blob_desde_archivo(self, nombre_archivo: str) -> ResultadoComando:

        try:
            archivo_path = self.directorio_trabajo / nombre_archivo
            
            if not archivo_path.exists():
                return ResultadoComando(
                    False,
                    f"El archivo '{nombre_archivo}' no existe"
                )
            
            if not archivo_path.is_file():
                return ResultadoComando(
                    False,
                    f"'{nombre_archivo}' no es un archivo válido"
                )
            
            # Leer contenido del archivo
            with open(archivo_path, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            # Crear blob
            blob = Blob(contenido)
            hash_blob = blob.compute_hash()
            
            # Guardar blob como objeto (si no existe)
            ruta_objeto_blob = self.directorio_objetos / hash_blob
            if not ruta_objeto_blob.exists():
                with open(ruta_objeto_blob, 'w', encoding='utf-8') as archivo:
                    archivo.write(blob.get_content())
            
            return ResultadoComando(
                True,
                "Blob creado exitosamente",
                {
                    "hash_blob": hash_blob,
                    "tamaño_contenido": len(contenido.encode('utf-8'))
                }
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al crear blob: {error}"
            )
    
    def crear_tree_directorio_actual(self) -> ResultadoComando:

        try:
            archivos = []
            directorios = []
            
            # Obtener archivos y directorios del directorio actual
            for item in self.directorio_trabajo.iterdir():
                if item.name.startswith('.'):
                    continue  # Ignorar archivos/directorios ocultos
                
                if item.is_file():
                    archivos.append(BlobEntry(item.name))
                elif item.is_dir():
                    directorios.append(TreeEntry(item.name))
            
            # Crear tree
            tree = Tree(archivos, directorios)
            hash_tree = tree.compute_hash()
            
            # Guardar tree como objeto
            ruta_objeto_tree = self.directorio_objetos / hash_tree
            with open(ruta_objeto_tree, 'w', encoding='utf-8') as archivo:
                archivo.write(tree.get_content())
            
            return ResultadoComando(
                True,
                "Tree creado exitosamente",
                {
                    "hash_tree": hash_tree,
                    "cantidad_entradas": len(archivos) + len(directorios)
                }
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al crear tree: {error}"
            )
    
    def mostrar_contenido_objeto(self, hash_objeto: str) -> ResultadoComando:

        try:
            if not self._verificar_repositorio_existe():
                return ResultadoComando(
                    False,
                    "No hay un repositorio Mini Git inicializado en este directorio"
                )
            
            ruta_objeto = self.directorio_objetos / hash_objeto
            
            if not ruta_objeto.exists():
                return ResultadoComando(
                    False,
                    f"El objeto con hash '{hash_objeto}' no existe"
                )
            
            # Leer contenido del objeto
            with open(ruta_objeto, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            # Detectar tipo de objeto
            tipo_objeto = self._detectar_tipo_objeto(contenido)
            
            return ResultadoComando(
                True,
                "Objeto encontrado",
                {
                    "tipo_objeto": tipo_objeto,
                    "contenido_objeto": contenido
                }
            )
        
        except Exception as error:
            return ResultadoComando(
                False,
                f"Error al mostrar objeto: {error}"
            )
    
    # Métodos auxiliares privados
    
    def _verificar_repositorio_existe(self) -> bool:

        return self.directorio_git.exists() and self.archivo_configuracion.exists()
    
    def _cargar_configuracion(self) -> dict:

        with open(self.archivo_configuracion, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    
    def _guardar_configuracion(self, configuracion: dict) -> None:

        with open(self.archivo_configuracion, 'w', encoding='utf-8') as archivo:
            json.dump(configuracion, archivo, indent=2, ensure_ascii=False)
    
    def _cargar_indice(self) -> dict:

        if not self.archivo_indice.exists():
            return {"archivos_preparados": {}, "ultima_actualizacion": ""}
        
        with open(self.archivo_indice, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    
    def _guardar_indice(self, indice: dict) -> None:

        with open(self.archivo_indice, 'w', encoding='utf-8') as archivo:
            json.dump(indice, archivo, indent=2, ensure_ascii=False)
    
    def _obtener_todos_archivos(self) -> List[str]:

        archivos = []
        for item in self.directorio_trabajo.iterdir():
            if item.name.startswith('.') or item.name == '.mini-git':
                continue
            if item.is_file():
                archivos.append(item.name)
        return archivos
    
    def _agregar_archivo_individual(self, nombre_archivo: str, indice: dict) -> bool:
        try:
            archivo_path = self.directorio_trabajo / nombre_archivo
            
            # Leer contenido y crear blob
            with open(archivo_path, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            blob = Blob(contenido)
            hash_blob = blob.compute_hash()
            
            # Guardar blob como objeto
            ruta_objeto_blob = self.directorio_objetos / hash_blob
            if not ruta_objeto_blob.exists():
                with open(ruta_objeto_blob, 'w', encoding='utf-8') as archivo:
                    archivo.write(blob.get_content())
            
            # Agregar al índice
            indice["archivos_preparados"][nombre_archivo] = {
                "hash": hash_blob,
                "tamaño": len(contenido.encode('utf-8'))
            }
            
            return True
        
        except Exception:
            return False
    
    def _obtener_informacion_autor(self, nombre: Optional[str], email: Optional[str]) -> dict:

        configuracion = self._cargar_configuracion()
        autor_predeterminado = configuracion.get("autor_predeterminado", {})
        
        nombre_final = nombre or autor_predeterminado.get("nombre")
        email_final = email or autor_predeterminado.get("email")
        
        if not nombre_final:
            return {
                "valido": False,
                "error": "Nombre del autor requerido. Usa --autor-nombre o configura un autor predeterminado."
            }
        
        if not email_final:
            return {
                "valido": False,
                "error": "Email del autor requerido. Usa --autor-email o configura un email predeterminado."
            }
        
        return {
            "valido": True,
            "nombre": nombre_final,
            "email": email_final
        }
    
    def _crear_tree_desde_indice(self, indice: dict) -> dict:

        try:
            blob_entries = []
            for nombre_archivo in indice["archivos_preparados"]:
                blob_entries.append(BlobEntry(nombre_archivo))
            
            tree = Tree(blob_entries, [])  # Por simplicidad, no manejamos subdirectorios
            hash_tree = tree.compute_hash()
            
            # Guardar tree como objeto
            ruta_objeto_tree = self.directorio_objetos / hash_tree
            with open(ruta_objeto_tree, 'w', encoding='utf-8') as archivo:
                archivo.write(tree.get_content())
            
            return {"exitoso": True, "hash": hash_tree}
        
        except Exception as error:
            return {"exitoso": False, "error": str(error)}
    
    def _obtener_ultimo_commit(self) -> Optional[str]:

        archivo_head = self.directorio_git / "HEAD"
        if archivo_head.exists():
            with open(archivo_head, 'r', encoding='utf-8') as archivo:
                return archivo.read().strip()
        return None
    
    def _actualizar_head(self, hash_commit: str) -> None:

        archivo_head = self.directorio_git / "HEAD"
        with open(archivo_head, 'w', encoding='utf-8') as archivo:
            archivo.write(hash_commit)
    
    def _obtener_informacion_commit(self, hash_commit: str) -> Optional[dict]:

        try:
            ruta_objeto = self.directorio_objetos / hash_commit
            if not ruta_objeto.exists():
                return None
            
            with open(ruta_objeto, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            # Parsear contenido del commit
            lineas = contenido.split('\n')
            info = {"hash": hash_commit}
            
            for linea in lineas:
                if linea.startswith("Author: "):
                    info["autor_nombre"] = linea[8:]
                elif linea.startswith("Email: "):
                    info["autor_email"] = linea[7:]
                elif linea.startswith("Date: "):
                    info["fecha"] = linea[6:]
                elif linea.startswith("Message: "):
                    info["mensaje"] = linea[9:]
                elif linea.startswith("Parent: "):
                    info["parent_hash"] = linea[8:]
            
            return info
        
        except Exception:
            return None
    
    def _detectar_tipo_objeto(self, contenido: str) -> str:

        if contenido.startswith("blob"):
            return "blob"
        elif contenido.startswith("tree"):
            return "tree"
        elif contenido.startswith("commit"):
            return "commit"
        else:
            return "desconocido"