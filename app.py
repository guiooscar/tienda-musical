from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from models.productos import (
    insertar_producto,
    obtener_productos_con_subcategoria,
    obtener_producto_por_id,
    actualizar_producto,
    eliminar_producto_por_id,
    buscar_productos_por_termino,
    obtener_todas_las_categorias,
    obtener_todas_las_subcategorias,
    obtener_subcategorias_por_categoria,
    obtener_subcategoria_por_id
)

from models.usuarios import obtener_usuario_por_username
from models.autenticacion import rol_requerido

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_segura'

# -------------------------------------------
# Login y logout
# -------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = obtener_usuario_por_username(username)

        if usuario and password == usuario['password']:  
            session['username'] = usuario['username']
            session['rol'] = usuario['rol']
            session['nombre_completo'] = usuario['nombre_completo']  
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------------------------------
# Página principal (restringida a logueados)
# -------------------------------------------

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# -------------------------------------------
# Productos: Agregar (solo admin)
# -------------------------------------------

@app.route('/agregar', methods=['GET', 'POST'])
@rol_requerido('admin')
def agregar_producto():
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
# Productos: Buscar (ambos roles)
# -------------------------------------------

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_producto():
    if 'username' not in session:
        return redirect(url_for('login'))

    productos = []
    if request.method == 'POST':
        productos = buscar_productos_por_termino(request.form['termino'])
    return render_template('buscar.html', productos=productos)

# -------------------------------------------
# Productos: Visualización (ambos roles)
# -------------------------------------------

@app.route('/productos')
def ver_productos():
    if 'username' not in session:
        return redirect(url_for('login'))

    page   = request.args.get('page', 1, type=int)
    cat    = request.args.get('cat', None, type=int)
    subcat = request.args.get('subcat', None, type=int)

    productos = obtener_productos_con_subcategoria()

    if cat:
        productos = [p for p in productos if p['id_categoria'] == cat]
    if subcat:
        productos = [p for p in productos if p['id_subcategoria'] == subcat]

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    prev_url = url_for('ver_productos', page=page-1, cat=cat, subcat=subcat) if page > 1 else None
    next_url = url_for('ver_productos', page=page+1, cat=cat, subcat=subcat) if end < len(productos) else None

    return render_template(
        'productos.html',
        productos=productos[start:end],
        prev_url=prev_url,
        next_url=next_url,
        categorias=obtener_todas_las_categorias(),
        subcategorias=obtener_todas_las_subcategorias(),
        cat=cat,
        subcat=subcat
    )

# -------------------------------------------
# Productos: Detalle (ambos roles)
# -------------------------------------------

@app.route('/producto/<int:id_producto>')
def detalle_producto(id_producto):
    if 'username' not in session:
        return redirect(url_for('login'))

    producto = obtener_producto_por_id(id_producto)
    return render_template('producto.html', producto=producto)

# -------------------------------------------
# Productos: Editar (solo admin)
# -------------------------------------------

@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
@rol_requerido('admin')
def editar_producto(id_producto):
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
    subcategoria = obtener_subcategoria_por_id(producto['id_subcategoria'])
    id_categoria_producto = subcategoria['id_categoria'] if subcategoria else None

    return render_template(
        'editar.html',
        producto=producto,
        categorias=obtener_todas_las_categorias(),
        subcategorias=obtener_todas_las_subcategorias(),
        id_categoria_producto=id_categoria_producto
    )

# -------------------------------------------
# Productos: Eliminar (solo admin)
# -------------------------------------------

@app.route('/eliminar/<int:id_producto>')
@rol_requerido('admin')
def eliminar_producto(id_producto):
    eliminar_producto_por_id(id_producto)
    return redirect(url_for('ver_productos'))

# -------------------------------------------
# Utilidades: Subcategorías dinámicas (AJAX)
# -------------------------------------------

@app.route('/subcategorias/<int:id_categoria>')
def get_subcats(id_categoria):
    return jsonify(obtener_subcategorias_por_categoria(id_categoria))

# -------------------------------------------
# Ejecutar la aplicación
# -------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
