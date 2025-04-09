from flask import jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import get_user_by_email, get_users, get_user_by_id, add_user, update_user, del_user, del_user_by_email, get_user_by_username, get_profile_by_user_id, update_profile, get_all_movies

# Definir rutas
def init_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = get_user_by_email(email)
            
            if user and user.password == password:  # En producción usar hash
                login_user(user)
                return redirect(url_for('index'))
            flash('Usuario o contraseña incorrectos')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        if request.method == 'POST':
            bio = request.form.get('bio')
            movie_id = request.form.get('movie_id')
            update_profile(current_user.id, bio, movie_id)
            flash('Perfil actualizado exitosamente')
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
