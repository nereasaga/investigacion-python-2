from flask import Flask
from flask_login import LoginManager
from routes import init_routes
from models import get_user_by_id

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para sesiones

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Nombre de la vista de login

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Registrar rutas
init_routes(app)  # Aquí se vinculan las rutas al proyecto

# if __name__ == '__main__':
#     app.run(debug=True)
