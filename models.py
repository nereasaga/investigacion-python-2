# Importar bibliotecas
import sqlite3
from flask_login import UserMixin

# Definir la tabla a la que conectar
table_name = 'users.db'

# Función para obtener una conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(table_name)
    conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios y nos deja acceder por nombre de la columnauser['username'] en vez de por id user[0]
    return conn

# Función para obtener los usuarios de la base de datos
def get_users():
    conn = get_db_connection()  # Uso de la función de conexión con el concepto de segmentación de código
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# Función para obtener un usuario por su ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
    return None

# Función para obtener un usuario por su nombre de usuario
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Función para obtener un usuario por su correo electrónico
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
    return None

# Función para agregar un nuevo usuario
def add_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()
    conn.close()

# Función para actualizar un usuario
def update_user(user_id, username=None, email=None, password=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First get the current user data
    cursor.execute('SELECT username, email, password FROM users WHERE id = ?', (user_id,))
    current_user = cursor.fetchone()
    
    if current_user:
        # Use new values if provided, otherwise keep current values
        new_username = username if username is not None else current_user['username']
        new_email = email if email is not None else current_user['email']
        new_password = password if password is not None else current_user['password']
        
        cursor.execute(
            'UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?',
            (new_username, new_email, new_password, user_id)
        )
        conn.commit()
    conn.close()

# Función para eliminar un usuario por su ID
def del_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# Función para eliminar un usuario por su correo electrónico
def del_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    conn.commit()
    conn.close()

