"""
Mini Git PyUI - Interfaz visual para el clon de GitHub Desktop
"""
import sys
import os
from pathlib import Path

# Agregar el directorio src al path para importar los módulos existentes
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from ui.ui_manager import UIManager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación Flask
app = Flask(__name__, 
            template_folder='ui/templates',
            static_folder='ui/static')

# Configurar clave secreta para sesiones
app.secret_key = 'mini-git-py-secret-key-dev'

# Instanciar el manejador de UI
ui_manager = UIManager()

@app.route('/')
def home():
    """
    Página principal que muestra la lista de repositorios locales
    """
    try:
        repositories = ui_manager.get_local_repositories()
        return render_template('home.html', repositories=repositories)
    except Exception as e:
        logger.error(f"Error en home: {e}")
        return render_template('home.html', repositories=[], error=str(e))

@app.route('/repository/<path:repo_path>')
def repository_view(repo_path):
    """
    Vista detallada de un repositorio específico
    """
    try:
        repo_data = ui_manager.get_repository_details(repo_path)
        if repo_data is None:
            return redirect(url_for('home'))
        
        return render_template('repository.html', 
                             repository=repo_data,
                             current_path=repo_path)
    except Exception as e:
        logger.error(f"Error en repository_view: {e}")
        return redirect(url_for('home'))

@app.route('/repository/<path:repo_path>/commits')
def commit_history(repo_path):
    """
    Vista del historial de commits de un repositorio
    """
    try:
        commits_data = ui_manager.get_commit_history(repo_path)
        repo_info = ui_manager.get_repository_info(repo_path)
        
        return render_template('commit_history.html',
                             commits=commits_data,
                             repository=repo_info,
                             current_path=repo_path)
    except Exception as e:
        logger.error(f"Error en commit_history: {e}")
        return redirect(url_for('home'))

@app.route('/api/repositories')
def api_repositories():
    """
    API endpoint para obtener la lista de repositorios
    """
    try:
        repositories = ui_manager.get_local_repositories()
        return jsonify({"status": "success", "data": repositories})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/repository/<path:repo_path>/status')
def api_repository_status(repo_path):
    """
    API endpoint para obtener el estado de un repositorio
    """
    try:
        status = ui_manager.get_repository_status(repo_path)
        return jsonify({"status": "success", "data": status})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/repository/<path:repo_path>/commit-graph')
def api_commit_graph(repo_path):
    """
    API endpoint para obtener datos del grafo de commits
    """
    try:
        graph_data = ui_manager.get_commit_graph_data(repo_path)
        return jsonify({"status": "success", "data": graph_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/clone', methods=['POST'])
def clone_repository():
    """
    Endpoint para clonar un repositorio
    """
    try:
        repo_url = request.form.get('repo_url')
        local_path = request.form.get('local_path')
        
        if not repo_url or not local_path:
            return jsonify({"status": "error", "message": "URL y ruta local son requeridos"})
        
        result = ui_manager.clone_repository(repo_url, local_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/create-repo', methods=['POST'])
def create_repository():
    """
    Endpoint para crear un nuevo repositorio
    """
    try:
        repo_name = request.form.get('repo_name')
        repo_path = request.form.get('repo_path')
        
        if not repo_name or not repo_path:
            return jsonify({"status": "error", "message": "Nombre y ruta son requeridos"})
        
        result = ui_manager.create_repository(repo_name, repo_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/commit', methods=['POST'])
def make_commit():
    """
    Endpoint para hacer un commit
    """
    try:
        repo_path = request.form.get('repo_path')
        message = request.form.get('commit_message')
        author = request.form.get('author', 'Usuario')
        email = request.form.get('email', 'usuario@ejemplo.com')
        
        if not repo_path or not message:
            return jsonify({"status": "error", "message": "Repositorio y mensaje son requeridos"})
        
        result = ui_manager.make_commit(repo_path, message, author, email)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.errorhandler(404)
def not_found_error(error):
    """Manejador de errores 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador de errores 500"""
    logger.error(f"Error interno: {error}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Crear directorios necesarios si no existen
    os.makedirs('ui/templates', exist_ok=True)
    os.makedirs('ui/static/css', exist_ok=True)
    os.makedirs('ui/static/js', exist_ok=True)
    os.makedirs('ui/static/icons', exist_ok=True)
    
    print("🚀 Iniciando Mini Git PyUI...")
    print("📁 Servidor disponible en: http://localhost:3000")
    print("🔥 Modo desarrollo activado")
    
    app.run(host='0.0.0.0', port=3000, debug=True)