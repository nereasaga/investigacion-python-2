from flask import Flask
from flask_login import LoginManager
from routes import init_routes
from models import get_user_by_id
from dotenv import load_dotenv
import os

app = Flask(__name__)


# Carga las variables del archivo .env (hay que tener instalado python-dotenv)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY no está configurada. Configúrala como variable de entorno.")

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'  # Nombre de la vista de login

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Registrar rutas
init_routes(app)  # Aquí se vinculan las rutas al proyecto

if __name__ == '__main__':
    app.run(debug=True)
