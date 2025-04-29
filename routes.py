from flask import jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import get_user_by_email, get_users, get_user_by_id, add_user, update_user, del_user, del_user_by_email, get_user_by_username, get_profile_by_user_id, update_profile, get_all_movies
import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import request, render_template, g
from time import time
import logging
from limite_peticiones import limite_peticiones

# Configurar logging
logging.basicConfig(level=logging.INFO)
filename='app.log',
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)

# Definir rutas

def init_routes(app):
    # Configuración para subida de archivos
    UPLOAD_FOLDER = 'static/avatars'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Asegurarse de que el directorio existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = get_user_by_email(email)
            
            if user and user.password == password:  # En producción usar hash
                login_user(user)
                return redirect(url_for('index'))
            flash('Usuario o contraseña incorrectos', 'error')
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        if request.method == 'POST':
            bio = request.form.get('bio')
            movie_id = request.form.get('movie_id')
            avatar_path = None
            
            # Procesar el archivo si fue enviado
            if 'avatar' in request.files:
                avatar = request.files['avatar']
                if avatar and allowed_file(avatar.filename):
                    # Crear nombre de archivo seguro
                    filename = secure_filename(f"user_{current_user.id}_{avatar.filename}")
                    # Guardar el archivo
                    avatar.save(os.path.join(UPLOAD_FOLDER, filename))
                    avatar_path = filename
            
            update_profile(current_user.id, bio, movie_id, avatar_path)
            flash('Perfil actualizado exitosamente', 'success')  # Añadimos categoría 'success'
            return redirect(url_for('dashboard'))

        profile = get_profile_by_user_id(current_user.id)
        movies = get_all_movies()
        return render_template('dashboard.html', profile=profile, movies=movies)
    
  # Vista de lista de usuarios
    @app.route('/users/view')
    @login_required
    def list_users_view():
        users = get_users()
        return render_template('users.html', users=users)

    # Vista de usuario individual
    @app.route('/users/view/<int:user_id>')
    @login_required
    def view_user(user_id):
        user = get_user_by_id(user_id)
        if user:
            profile = get_profile_by_user_id(user_id)  # Obtener el perfil del usuario
            return render_template('user_detail.html', user=user, profile=profile)
        return redirect(url_for('list_users_view'))    
    
    
# API REST con json como respuesta    
    
    
    # Rutas para obtener todos los usuarios
    @app.route('/users')
    def list_users():
        users = get_users()  # Usa la función que encapsula la conexión
        return jsonify([dict(user) for user in users])

    # Rutas para obtener un usuario por su ID
    @app.route('/users/<int:user_id>')
    def get_user_by_id_route(user_id):
        user = get_user_by_id(user_id)
        if user:
            return jsonify(dict(user))
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    
    # Rutas para crear usuarios   
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        add_user(username, email, password)
        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    # Rutas para actualizar usuarios totalmente
    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user_route(user_id):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        update_user(user_id, username, email, password)
        return jsonify({'message': 'Usuario actualizado exitosamente'})

    # Rutas para actualizar usuarios parcialmente
    @app.route('/users/<int:user_id>', methods=['PATCH'])
    def update_user_partial_route(user_id):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        update_user(user_id, username, email, password)
        return jsonify({'message': 'Usuario actualizado exitosamente'})

    # Rutas para eliminar usuarios por id
    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        del_user(user_id)
        return jsonify({'message': 'Usuario eliminado exitosamente'})   

    # Rutas para eliminar usuarios por email
    @app.route('/users/email/<string:email>', methods=['DELETE'])
    def delete_user_by_email(email):
        del_user_by_email(email)
        return jsonify({'message': 'Usuario eliminado exitosamente'})   

    @app.route('/users/add', methods=['GET'])
    @login_required
    def add_user_view():
        return render_template('add_user.html')

    # Decorador personalizado para medir tiempo de ejecución
    def medir_tiempo(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            inicio = time()
            resultado = f(*args, **kwargs)
            fin = time()
            tiempo_total = fin - inicio
            logger.info(f'La función {f.__name__} tardó {tiempo_total:.4f} segundos')
            return resultado
        return decorated_function

    # Ejemplo de @app.before_request
    @app.before_request
    def antes_de_request():
        g.inicio_request = time()
        g.mensaje_before = "¡Esto se ejecutó antes del request!"

    # Ejemplo de @app.after_request
    @app.after_request
    def despues_de_request(response):
        if hasattr(g, 'inicio_request'):
            tiempo_total = time() - g.inicio_request
            response.headers['X-Tiempo-Ejecución de after_request'] = str(tiempo_total)
        return response

    # Ejemplo de @app.errorhandler
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('error.html', 
                             error_code=404, 
                             mensaje="¡Ups! Página no encontrada"), 404

    # Ruta que muestra ejemplos de decoradores
    @app.route('/decoradores')
    @medir_tiempo
    def ejemplos_decoradores():
        # Simulamos un error 404
        mostrar_404 = request.args.get('error404', False)
        if mostrar_404:
            # Forma correcta de generar un error 404
            abort(404)

        # Datos para mostrar en la plantilla
        datos = {
            'mensaje_before': g.mensaje_before,
            'tiempo_inicio': g.inicio_request,
            'tiempo_actual': time()
        }
        
        return render_template('decoradores.html', datos=datos)

    #decorador para limitar nº de peticviones al endpoint recurso-limitado
    @app.route('/recurso-limitado')
    @limite_peticiones(max_peticiones=5, periodo=60)
    def recurso_limitado():
        # Renderizamos una plantilla que extiende de base.html
        return render_template('recurso_limitado.html')
    


    #Obtener profile
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            g.profile = get_profile_by_user_id(current_user.id)
        else:
            g.profile = None

    # Modificar el contexto de todas las plantillas
    @app.context_processor
    def inject_profile():
        return dict(profile=g.profile)
