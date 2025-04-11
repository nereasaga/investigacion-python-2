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

## Tests

Para ejecutar los tests:
```bash
pytest tests/
```

## Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
