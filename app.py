from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.productos import (
    insertar_producto,
    obtener_productos_con_subcategoria,
    obtener_producto_por_id,
    actualizar_producto,
    eliminar_producto_por_id,
    buscar_productos_por_termino,
    obtener_todas_las_categorias,
    obtener_todas_las_subcategorias,
    obtener_subcategorias_por_categoria
)

# Inicialización de la aplicación Flask
app = Flask(__name__)

# -------------------------------------------
# Rutas principales
# -------------------------------------------

@app.route('/')
def index():
    """Página de inicio del panel de administración."""
    return render_template('index.html')

# -------------------------------------------
# Productos: Agregar
# -------------------------------------------

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    """Agrega un nuevo producto a la base de datos."""
    if request.method == 'POST':
        insertar_producto(
            request.form['id_subcategoria'],
            request.form['nombre'],
            request.form['referencia'],
            request.form['descripcion'],
            request.form['precio'],
            request.form['cantidad'],
            request.form['img_url']
        )
        return redirect(url_for('ver_productos'))
    return render_template(
        'agregar.html',
        categorias=obtener_todas_las_categorias(),
        subcategorias=obtener_todas_las_subcategorias()
    )

# -------------------------------------------
# Productos: Buscar
# -------------------------------------------

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_producto():
    """Busca productos por nombre o referencia."""
    productos = []
    if request.method == 'POST':
        productos = buscar_productos_por_termino(request.form['termino'])
    return render_template('buscar.html', productos=productos)

# -------------------------------------------
# Productos: Visualización y paginación
# -------------------------------------------

@app.route('/productos')
def ver_productos():
    """Visualiza todos los productos con opciones de paginación y filtrado."""
    page   = request.args.get('page', 1, type=int)
    cat    = request.args.get('cat', None, type=int)
    subcat = request.args.get('subcat', None, type=int)

    productos = obtener_productos_con_subcategoria()
    # Filtrado por categoría y subcategoría
    if cat:
        productos = [p for p in productos if p['id_categoria'] == cat]
    if subcat:
        productos = [p for p in productos if p['id_subcategoria'] == subcat]

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    productos_pag = productos[start:end]
    # se usa el mismo nombre de la función para la URL de paginación
    prev_url = url_for('ver_productos', page=page-1, cat=cat, subcat=subcat) if page > 1 else None
    next_url = url_for('ver_productos', page=page+1, cat=cat, subcat=subcat) if end < len(productos) else None

    return render_template(
        'productos.html',
        productos=productos_pag,
        prev_url=prev_url,
        next_url=next_url,
        categorias=obtener_todas_las_categorias(),
        subcategorias=obtener_todas_las_subcategorias(),
        cat=cat,
        subcat=subcat
    )

# -------------------------------------------
# Productos: Detalle
# -------------------------------------------

@app.route('/producto/<int:id_producto>')
def detalle_producto(id_producto):
    """Muestra el detalle de un producto específico."""
    producto = obtener_producto_por_id(id_producto)
    return render_template('producto.html', producto=producto)

# -------------------------------------------
# Productos: Editar
# -------------------------------------------

@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    """Edita un producto existente."""
    if request.method == 'POST':
        actualizar_producto(
            id_producto,
            request.form['id_subcategoria'],
            request.form['nombre'],
            request.form['referencia'],
            request.form['descripcion'],
            request.form['precio'],
            request.form['cantidad'],
            request.form['img_url']
        )
        return redirect(url_for('ver_productos'))
    producto = obtener_producto_por_id(id_producto)
    return render_template(
        'editar.html',
        producto=producto,
        categorias=obtener_todas_las_categorias(),
        subcategorias=obtener_todas_las_subcategorias()
    )

# -------------------------------------------
# Productos: Eliminar
# -------------------------------------------

@app.route('/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):
    """Elimina un producto por su ID."""
    eliminar_producto_por_id(id_producto)
    return redirect(url_for('ver_productos'))

# -------------------------------------------
# Utilidades: Obtener subcategorías dinámicas
# -------------------------------------------

@app.route('/subcategorias/<int:id_categoria>')
def get_subcats(id_categoria):
    """Devuelve subcategorías en formato JSON dado un id_categoria (AJAX)."""
    return jsonify(obtener_subcategorias_por_categoria(id_categoria))

# -------------------------------------------
# Ejecutar la aplicación
# -------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
