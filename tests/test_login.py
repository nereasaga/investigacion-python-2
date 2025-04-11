import pytest
from models import get_users, get_user_by_email  # Importa las funciones necesarias
from flask_login import login_user
from app import app  # Importa la instancia de Flask desde app.py

# Test para verificar el inicio de sesión de todos los usuarios
def test_login_all_users():
    # Crear un contexto de aplicación y solicitud
    with app.app_context(), app.test_request_context():
        # Obtener todos los usuarios de la base de datos
        users = get_users()

        # Verificar que hay usuarios en la base de datos
        assert len(users) > 0, "No se encontraron usuarios en la base de datos."

        # Iterar sobre cada usuario y verificar el inicio de sesión
        for user in users:
            # Extraer los datos del usuario
            email = user['email']
            password = user['password']

            # Buscar el usuario por su correo electrónico
            db_user = get_user_by_email(email)

            # Verificar que el usuario existe en la base de datos
            assert db_user is not None, f"El usuario con email {email} no existe en la base de datos."

            # Verificar que la contraseña coincide
            assert db_user.password == password, f"La contraseña no coincide para el usuario {email}."

            # Simular el inicio de sesión
            login_user(db_user)

            # Verificar que el usuario está autenticado
            assert db_user.is_authenticated, f"El usuario {email} no se ha autenticado correctamente."