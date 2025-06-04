# -------------------------------------------
# usuarios.py
# Módulo de acceso a datos para autenticación y roles
# -------------------------------------------

from conexion import obtener_conexion

def obtener_usuario_por_username(username):
    """Busca un usuario en la base de datos por su nombre de usuario."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario
