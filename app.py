from flask import Flask
from routes import init_routes  # Importa función que define rutas

app = Flask(__name__)

# Registrar rutas
init_routes(app)  # Aquí se vinculan las rutas al proyecto

if __name__ == '__main__':
    app.run(debug=True)