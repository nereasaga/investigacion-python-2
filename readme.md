# Gestión de Usuarios con Flask

Aplicación web desarrollada con Flask para la gestión de usuarios, que incluye funcionalidades de autenticación, perfiles de usuario y gestión de avatares, bio y selección de la película favorita de los Monty Python. 

## Características

- Sistema de autenticación (login/logout)
- Gestión de perfiles de usuario
- Subida de avatares
- Dashboard personalizado
- Lista de usuarios con operaciones CRUD
- API REST para operaciones con usuarios
- Ejemplos de uso de decoradores en Flask

## Requisitos

- Python 3.x
- Flask
- Flask-Login
- SQLite3

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Inicializa la base de datos:
```bash
python creartablas.py
```

4. Ejecuta la aplicación:
```bash
python app.py
```

## Estructura del Proyecto

```
├── app.py                 # Punto de entrada de la aplicación
├── routes.py             # Definición de rutas
├── models.py             # Modelos de datos
├── creartablas.py        # Script para inicializar la BD
├── static/              
│   ├── css/             # Estilos CSS
│   └── avatars/         # Almacenamiento de avatares
├── templates/            # Plantillas HTML
└── tests/               # Tests unitarios
```
## API REST con Flask
Este proyecto implementa una API RESTful con Flask que permite gestionar usuarios mediante peticiones HTTP y devuelve respuestas en formato JSON. Incluye funcionalidades CRUD completas, manejo de errores, decoradores personalizados y middleware para controlar tiempos de ejecución y contexto de plantillas.

🚀 Funcionalidades principales

    🔍 Obtener todos los usuarios (GET /users)

    🔍 Obtener usuario por ID (GET /users/<id>)

    ➕ Crear nuevo usuario (POST /users)

    ✏️ Actualizar usuario completamente (PUT /users/<id>)

    🛠️ Actualizar usuario parcialmente (PATCH /users/<id>)

    🗑️ Eliminar usuario por ID (DELETE /users/<id>)

    🗑️ Eliminar usuario por email (DELETE /users/email/<email>)

🧰 Extras incluidos

    Página web para añadir usuarios desde el navegador (GET /users/add)

    Decorador personalizado @medir_tiempo para medir tiempo de ejecución de funciones

    Middleware con @before_request y @after_request para registrar tiempos y modificar respuestas

    Manejador de errores (@app.errorhandler(404)) con renderizado de plantilla personalizada

    Inyección automática de datos del perfil de usuario en todas las plantillas mediante @context_processor

🔐 Autenticación y contexto

    Soporte para login_required en rutas protegidas

    Carga automática del perfil del usuario autenticado en cada request (g.profile)
    
🖥️ Vistas HTML

Además de las rutas API, también se implementan vistas para visualizar usuarios y perfiles a través de páginas web:

    Vista de lista de usuarios: Muestra todos los usuarios registrados en la base de datos.

        Ruta: /users/view

        Requiere autenticación mediante el decorador @login_required.

        Usa la plantilla users.html para mostrar la lista de usuarios.

        ```bash
@app.route('/users/view')
@login_required
def list_users_view():
    users = get_users()
    return render_template('users.html', users=users)

```

Vista de usuario individual: Muestra la información detallada de un usuario junto con su perfil.

    Ruta: /users/view/<int:user_id>

    Requiere autenticación mediante el decorador @login_required.

    Si el usuario existe, se muestra su información y perfil en la plantilla user_detail.html. En caso contrario, redirige a la vista de lista de usuarios.

   ```bash
@app.route('/users/view/<int:user_id>')
@login_required
def view_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        profile = get_profile_by_user_id(user_id)  # Obtener el perfil del usuario
        return render_template('user_detail.html', user=user, profile=profile)
    return redirect(url_for('list_users_view'))

```
    
## Pruebas con Pytest
Este proyecto incluye pruebas automatizadas utilizando pytest para verificar el correcto funcionamiento de las funciones y las rutas. Se han creado los siguientes archivos de pruebas:

    test_main.py: Contiene pruebas para las funciones básicas como suma y is_greater_than, así como un ejemplo de prueba con parámetros y validación de login:

        test_suma(): Verifica que la función suma funciona correctamente.

        test_is_greater_than(): Verifica que is_greater_than devuelva True si el primer número es mayor que el segundo.

        test_suma_params(): Usa pytest.mark.parametrize para probar varias combinaciones de entrada en la función suma.

        test_login_pass(): Verifica el login correcto.

        test_login_fail(): Verifica el login fallido.

    test_ejemplo.py: Contiene pruebas para funciones matemáticas simples como suma, resta, multiplicación y división:

        test_add(): Verifica que la función add devuelve el resultado correcto.

        test_subtract(): Verifica que la función subtract funciona correctamente.

        test_multiply(): Verifica que la función multiply multiplica correctamente.

        test_divide(): Verifica que la función divide calcula correctamente, y lanza un error si se intenta dividir por cero.

Para ejecutar los tests:

```bash
pip install pytest
```

```bash
pytest -v
```

## Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
