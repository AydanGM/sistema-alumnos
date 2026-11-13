"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## @var app
# Aplicación Flask principal.
app = Flask(__name__)

## @var ALUMNOS
# Base de datos en memoria (solo para fines de la actividad)
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## @var VERSION
# La versión la inyecta el pipeline (ver Jenkinsfile). Sirve para la trazabilidad.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Endpoint para saludar al usuario.

    El nombre del usuario se extrae a través del parámetro 'name' recibido en la URL (query string)

    @return Mensaje de saludo que incluye el nombre entregado.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')

def health():
    """!
    @brief Verifica el estado de salud de la API.

    @return JSON con el estado 'ok'
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Retorna la versión actual de la aplicación.

    @return JSON con el nombre de la aplicación y la versión actual configurada.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Obtiene la lista completa de alumnos.

    @return JSON con la lista de todos los alumnos registrados en el sistema.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Obtiene un alumno por su identificador.

    @param alumno_id Identificador numérico del alumno.
    @return JSON con el alumno, o error 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Crea un nuevo registro de alumno en el sistema

    Espera un payload en formato JSON con los campos 'nombre, 'promedio' y opcionalmente 'carrera'

    @return JSON con los datos del alumno creado y código 201, o error 400 si los datos son inválidos.
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201

## @cond DOXYGEN_IGNORE
if __name__ == '__main__':
    app.run(debug=True)
## @endcond
