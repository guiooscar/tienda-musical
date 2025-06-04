# models/autenticacion.py
from functools import wraps
from flask import session, redirect, url_for

def rol_requerido(rol):
    """
    Decorador para restringir acceso a una ruta según el rol del usuario.

    Uso:
        @rol_requerido('admin')
    """
    def decorador(func):
        @wraps(func)
        def funcion_restringida(*args, **kwargs):
            if 'username' not in session or session.get('rol') != rol:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return funcion_restringida
    return decorador
