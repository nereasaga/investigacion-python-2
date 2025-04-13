from functools import wraps
from flask import request, make_response, render_template
import time


# Diccionario para almacenar el contador de peticiones por dirección IP
peticiones = {}

def limite_peticiones(max_peticiones, periodo=60):
    """
    Decorador personalizado para limitar el número de peticiones a una ruta.

    Args:
        max_peticiones (int): Número máximo de peticiones permitidas.
        periodo (int): Intervalo de tiempo en segundos para la cuota (por defecto, 60 segundos).
    """
    def midecorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            ip_cliente = request.remote_addr
            tiempo_actual = time.time()

            if ip_cliente not in peticiones:
                peticiones[ip_cliente] = []

            # Filtrar peticiones que están dentro del periodo
            peticiones[ip_cliente] = [t for t in peticiones[ip_cliente] if tiempo_actual - t < periodo]

            # Verificar cuota
            if len(peticiones[ip_cliente]) >= max_peticiones:
                # Cuando se llega al limite de peticiones mostramos la pantilla. El mensaje recoge la ip del solicitante y un text
                return render_template("error_peticiones.html", mensaje=f"Demasiadas peticiones desde la dirección IP: {ip_cliente}. Intenta más tarde."), 429

            peticiones[ip_cliente].append(tiempo_actual)

            # Agregar header opcional
            response = make_response(f(*args, **kwargs))
            response.headers["X-RateLimit-Remaining"] = max_peticiones - len(peticiones[ip_cliente])
            return response
        return funcion_decorada
    return midecorador
