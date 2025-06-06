# -------------------------------------------
# productos.py
# Módulo de acceso a datos para productos, categorías y subcategorías
# -------------------------------------------

from conexion import obtener_conexion

# -------------------------------------------
# Productos
# -------------------------------------------

def insertar_producto(id_subcategoria, nombre, referencia, descripcion, precio, cantidad, img_url):
    """Inserta un nuevo producto en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (id_subcategoria, nombre, referencia, descripcion, precio, cantidad, img_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_subcategoria, nombre, referencia, descripcion, precio, cantidad, img_url))
    conexion.commit()
    conexion.close()


def obtener_productos_con_subcategoria():
    """Obtiene todos los productos junto con el nombre de su subcategoría."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.id_producto, 
            p.nombre, 
            p.referencia,
            p.descripcion,
            p.precio, 
            p.cantidad, 
            p.img_url,
            s.nombre_subcategoria AS subcategoria,
            s.id_categoria AS id_categoria,
            s.id_subcategoria AS id_subcategoria
        FROM productos p
        JOIN subcategorias s ON p.id_subcategoria = s.id_subcategoria
    """)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_producto_por_id(id_producto):
    """Obtiene un producto por su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def actualizar_producto(id_producto, id_subcategoria, nombre, referencia, descripcion, precio, cantidad, img_url):
    """Actualiza un producto existente en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos
        SET id_subcategoria = %s, nombre = %s, referencia = %s, descripcion = %s,
            precio = %s, cantidad = %s, img_url = %s
        WHERE id_producto = %s
    """, (id_subcategoria, nombre, referencia, descripcion, precio, cantidad, img_url, id_producto))
    conexion.commit()
    conexion.close()


def eliminar_producto_por_id(id_producto):
    """Elimina un producto según su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()
    conexion.close()


def buscar_productos_por_termino(termino):
    """Busca productos por coincidencia en nombre o referencia."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id_producto, p.nombre, p.precio, p.cantidad, s.nombre_subcategoria AS subcategoria
        FROM productos p
        JOIN subcategorias s ON p.id_subcategoria = s.id_subcategoria
        WHERE p.nombre LIKE %s OR p.referencia LIKE %s
    """, (f"%{termino}%", f"%{termino}%"))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

# -------------------------------------------
# Categorías y Subcategorías
# -------------------------------------------

def obtener_todas_las_categorias():
    """Obtiene todas las categorías disponibles."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_todas_las_subcategorias():
    """Obtiene todas las subcategorías con su categoría asociada."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_subcategoria, nombre_subcategoria, id_categoria FROM subcategorias")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_subcategorias_por_categoria(id_categoria):
    """Obtiene las subcategorías pertenecientes a una categoría específica."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_subcategoria, nombre_subcategoria
        FROM subcategorias
        WHERE id_categoria = %s
    """, (id_categoria,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def obtener_subcategoria_por_id(id_subcategoria):
    """Obtiene la información de una subcategoría específica."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_subcategoria, nombre_subcategoria, id_categoria
        FROM subcategorias
        WHERE id_subcategoria = %s
    """, (id_subcategoria,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
