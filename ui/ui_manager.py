"""
UIManager - Controlador que conecta la lógica de negocio con la interfaz visual
"""
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Importar modelos y lógica existente
from implementations.repository import LocalRepository
from implementations.filesystem_store import FileSystemStore
from implementations.utf8_encoder import Utf8Encoder
from implementations.gzip_compressor import GzipCompressor
from implementations.object_serializer import ObjectSerializer
from models.commit import Commit
from models.hash import Sha256Hash
from models.email import Email
from models.ref import CommitRef

logger = logging.getLogger(__name__)

class UIManager:
    """
    Manejador de la interfaz de usuario que conecta la lógica de negocio
    con la capa visual Flask
    """
    
    def __init__(self):
        """
        Inicializa el manejador de UI
        """
        self._repositories_cache = {}
        self._file_store = FileSystemStore()
        self._encoder = Utf8Encoder()
        self._compressor = GzipCompressor()
        # ObjectSerializer maneja todos los tipos de serialización
        self._serializer = ObjectSerializer(self._encoder)
        self._blob_serializer = self._serializer
        self._tree_serializer = self._serializer
        self._commit_serializer = self._serializer
        self._tag_serializer = self._serializer
    
    def _get_repository_instance(self, repo_path: str) -> Optional[LocalRepository]:
        """
        Obtiene una instancia del repositorio local
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Instancia de LocalRepository o None si no existe
        """
        try:
            path = Path(repo_path)
            if not path.exists():
                return None
                
            # Verificar si es un repositorio válido (tiene carpeta .git o similar)
            git_dir = path / '.mini-git'
            if not git_dir.exists():
                return None
                
            return LocalRepository(
                file_store=self._file_store,
                encoder=self._encoder,
                blob_serializer=self._blob_serializer,
                tree_serializer=self._tree_serializer,
                commit_serializer=self._commit_serializer,
                tag_serializer=self._tag_serializer,
                compressor=self._compressor,
                base_dir=git_dir
            )
        except Exception as e:
            logger.error(f"Error obteniendo instancia de repositorio: {e}")
            return None
    
    def get_local_repositories(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de repositorios locales
        
        Returns:
            Lista de diccionarios con información de repositorios
        """
        repositories = []
        
        # Buscar repositorios en directorios comunes
        search_paths = [
            Path.home() / "Documents" / "GitHub",
            Path.home() / "Documents" / "Repositories",
            Path.home() / "git",
            Path.cwd().parent,
            Path.cwd()
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            try:
                for item in search_path.iterdir():
                    if item.is_dir():
                        # Verificar si tiene .mini-git o .git
                        if (item / '.mini-git').exists() or (item / '.git').exists():
                            repo_info = {
                                'name': item.name,
                                'path': str(item),
                                'last_modified': datetime.fromtimestamp(
                                    item.stat().st_mtime
                                ).strftime('%Y-%m-%d %H:%M:%S'),
                                'type': 'mini-git' if (item / '.mini-git').exists() else 'git'
                            }
                            repositories.append(repo_info)
            except (PermissionError, OSError) as e:
                logger.warning(f"No se pudo acceder a {search_path}: {e}")
                continue
        
        # Eliminar duplicados basándose en la ruta
        seen_paths = set()
        unique_repos = []
        for repo in repositories:
            if repo['path'] not in seen_paths:
                seen_paths.add(repo['path'])
                unique_repos.append(repo)
        
        return sorted(unique_repos, key=lambda x: x['last_modified'], reverse=True)
    
    def get_repository_details(self, repo_path: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalles completos de un repositorio
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Diccionario con detalles del repositorio o None
        """
        try:
            repo = self._get_repository_instance(repo_path)
            if not repo:
                return None
            
            # Información básica
            path = Path(repo_path)
            details = {
                'name': path.name,
                'path': repo_path,
                'type': 'mini-git',
                'status': self.get_repository_status(repo_path),
                'branches': self._get_branches(repo),
                'recent_commits': self._get_recent_commits(repo, limit=10),
                'file_count': self._count_tracked_files(repo_path),
                'last_commit': self._get_last_commit(repo)
            }
            
            return details
        except Exception as e:
            logger.error(f"Error obteniendo detalles del repositorio: {e}")
            return None
    
    def get_repository_status(self, repo_path: str) -> Dict[str, Any]:
        """
        Obtiene el estado actual de un repositorio
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Diccionario con el estado del repositorio
        """
        try:
            repo = self._get_repository_instance(repo_path)
            if not repo:
                return {'status': 'error', 'message': 'Repositorio no encontrado'}
            
            # Obtener HEAD actual
            try:
                head = repo.load_head()
                current_branch = head.name
            except:
                current_branch = 'main'  # Branch por defecto
            
            # Simular archivos modificados (en una implementación real esto vendría del working directory)
            modified_files = []
            staged_files = []
            untracked_files = []
            
            return {
                'current_branch': current_branch,
                'modified_files': modified_files,
                'staged_files': staged_files,
                'untracked_files': untracked_files,
                'clean': len(modified_files) == 0 and len(staged_files) == 0,
                'ahead': 0,  # commits ahead of remote
                'behind': 0  # commits behind remote
            }
        except Exception as e:
            logger.error(f"Error obteniendo estado del repositorio: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_commit_history(self, repo_path: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de commits de un repositorio
        
        Args:
            repo_path: Ruta al repositorio
            limit: Número máximo de commits a obtener
            
        Returns:
            Lista de commits con su información
        """
        try:
            repo = self._get_repository_instance(repo_path)
            if not repo:
                return []
            
            return self._get_recent_commits(repo, limit)
        except Exception as e:
            logger.error(f"Error obteniendo historial de commits: {e}")
            return []
    
    def get_commit_graph_data(self, repo_path: str) -> Dict[str, Any]:
        """
        Obtiene datos para el grafo de commits
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Datos del grafo de commits para visualización
        """
        try:
            commits = self.get_commit_history(repo_path, limit=100)
            
            # Crear nodos y enlaces para el grafo
            nodes = []
            links = []
            
            for i, commit in enumerate(commits):
                nodes.append({
                    'id': commit['sha'][:8],
                    'label': commit['message'][:50] + ('...' if len(commit['message']) > 50 else ''),
                    'author': commit['author'],
                    'date': commit['date'],
                    'full_sha': commit['sha']
                })
                
                # Crear enlaces con los padres
                for parent in commit.get('parents', []):
                    if any(n['full_sha'] == parent for n in nodes):
                        links.append({
                            'source': commit['sha'][:8],
                            'target': parent[:8]
                        })
            
            return {
                'nodes': nodes,
                'links': links
            }
        except Exception as e:
            logger.error(f"Error generando datos del grafo: {e}")
            return {'nodes': [], 'links': []}
    
    def get_repository_info(self, repo_path: str) -> Dict[str, Any]:
        """
        Obtiene información básica de un repositorio
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Información básica del repositorio
        """
        path = Path(repo_path)
        return {
            'name': path.name,
            'path': repo_path,
            'type': 'mini-git' if (path / '.mini-git').exists() else 'git'
        }
    
    def clone_repository(self, repo_url: str, local_path: str) -> Dict[str, Any]:
        """
        Clona un repositorio (simulado por ahora)
        
        Args:
            repo_url: URL del repositorio a clonar
            local_path: Ruta local donde clonar
            
        Returns:
            Resultado de la operación
        """
        try:
            # Por ahora simular la clonación
            path = Path(local_path)
            path.mkdir(parents=True, exist_ok=True)
            
            # Crear estructura básica de mini-git
            mini_git_dir = path / '.mini-git'
            mini_git_dir.mkdir(exist_ok=True)
            (mini_git_dir / 'objects').mkdir(exist_ok=True)
            (mini_git_dir / 'refs').mkdir(exist_ok=True)
            
            return {
                'status': 'success',
                'message': f'Repositorio clonado exitosamente en {local_path}',
                'path': local_path
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error clonando repositorio: {str(e)}'
            }
    
    def create_repository(self, repo_name: str, repo_path: str) -> Dict[str, Any]:
        """
        Crea un nuevo repositorio
        
        Args:
            repo_name: Nombre del repositorio
            repo_path: Ruta donde crear el repositorio
            
        Returns:
            Resultado de la operación
        """
        try:
            full_path = Path(repo_path) / repo_name
            full_path.mkdir(parents=True, exist_ok=True)
            
            # Crear estructura de mini-git
            mini_git_dir = full_path / '.mini-git'
            mini_git_dir.mkdir(exist_ok=True)
            (mini_git_dir / 'objects').mkdir(exist_ok=True)
            (mini_git_dir / 'refs').mkdir(exist_ok=True)
            (mini_git_dir / 'refs' / 'commits').mkdir(exist_ok=True)
            (mini_git_dir / 'refs' / 'tags').mkdir(exist_ok=True)
            
            # Crear archivo HEAD inicial
            (mini_git_dir / 'head').write_text('main\n')
            
            return {
                'status': 'success',
                'message': f'Repositorio "{repo_name}" creado exitosamente',
                'path': str(full_path)
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error creando repositorio: {str(e)}'
            }
    
    def make_commit(self, repo_path: str, message: str, author: str, email: str) -> Dict[str, Any]:
        """
        Realiza un commit en el repositorio
        
        Args:
            repo_path: Ruta al repositorio
            message: Mensaje del commit
            author: Autor del commit
            email: Email del autor
            
        Returns:
            Resultado de la operación
        """
        try:
            repo = self._get_repository_instance(repo_path)
            if not repo:
                return {'status': 'error', 'message': 'Repositorio no encontrado'}
            
            # Por ahora simular el commit
            # En una implementación real aquí se crearían los objetos blob, tree y commit
            
            return {
                'status': 'success',
                'message': f'Commit realizado exitosamente: "{message}"',
                'sha': 'abc123def456'  # SHA simulado
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error realizando commit: {str(e)}'
            }
    
    def _get_branches(self, repo: LocalRepository) -> List[str]:
        """
        Obtiene las ramas del repositorio
        
        Args:
            repo: Instancia del repositorio
            
        Returns:
            Lista de nombres de ramas
        """
        try:
            # En una implementación real, esto obtendría las ramas de refs/commits
            return ['main', 'develop']  # Ramas simuladas
        except Exception:
            return ['main']
    
    def _get_recent_commits(self, repo: LocalRepository, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene los commits más recientes
        
        Args:
            repo: Instancia del repositorio
            limit: Número máximo de commits
            
        Returns:
            Lista de commits
        """
        try:
            # Por ahora simular commits
            # En una implementación real, esto recorrería el grafo de commits
            commits = []
            for i in range(min(limit, 5)):  # Simular hasta 5 commits
                commits.append({
                    'sha': f'abcd{i:04d}ef{i*2:04d}',
                    'message': f'Commit de ejemplo #{i+1}',
                    'author': 'Usuario Ejemplo',
                    'email': 'usuario@ejemplo.com',
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'parents': [f'abcd{i-1:04d}ef{(i-1)*2:04d}'] if i > 0 else []
                })
            return commits
        except Exception:
            return []
    
    def _get_last_commit(self, repo: LocalRepository) -> Optional[Dict[str, Any]]:
        """
        Obtiene el último commit
        
        Args:
            repo: Instancia del repositorio
            
        Returns:
            Información del último commit o None
        """
        try:
            commits = self._get_recent_commits(repo, limit=1)
            return commits[0] if commits else None
        except Exception:
            return None
    
    def _count_tracked_files(self, repo_path: str) -> int:
        """
        Cuenta los archivos rastreados en el repositorio
        
        Args:
            repo_path: Ruta al repositorio
            
        Returns:
            Número de archivos rastreados
        """
        try:
            path = Path(repo_path)
            count = 0
            for item in path.rglob('*'):
                if item.is_file() and '.mini-git' not in str(item):
                    count += 1
            return count
        except Exception:
            return 0