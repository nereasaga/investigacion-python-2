from flask import jsonify, request
from models import get_users, get_user_by_id, add_user, update_user, del_user, del_user_by_email  # Importa la función modular

# Definir rutas
def init_routes(app):
    # Ruta de inicio
    @app.route('/')
    def index():
        return '<h1>Bienvenido a nuestra API de usuarios!</h1><p>Para ver la lista de usuarios, visita /users</p><p>Para ver un usuario en particular, visita /users/<id></p>'

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

