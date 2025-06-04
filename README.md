titulo: Tienda Musical
descripcion: >
  Este proyecto es una aplicación web creada con Flask para la gestión de inventario de una tienda de instrumentos musicales.
  Permite registrar, consultar y administrar productos como guitarras, bajos, teclados y más.

tecnologias_utilizadas:
  - Python 3
  - Flask
  - HTML/CSS
  - Jinja2
  - MySQL (con PHPMyAdmin en XAMPP)

estructura_del_proyecto: |
  tienda_musical/
  ├── app/
  ├── models/
  ├── static/
  ├── templates/
  ├── venv/             ← ignorado con .gitignore
  ├── conexion.py
  ├── requirements.txt
  ├── README.md

como_ejecutar:
  - paso: Clona el repositorio
    comando: |
      git clone https://github.com/guiooscar/tienda-musical.git

  - paso: Crea y activa un entorno virtual
    comando: |
      python -m venv venv
      venv\Scripts\activate

  - paso: Instala las dependencias
    comando: |
      pip install -r requirements.txt

  - paso: Ejecuta la app
    comando: |
      python app.py

estado_del_proyecto:
  descripcion: En desarrollo. Próximas funciones
  tareas_pendientes:
    - CRUD completo desde interfaz
    - Conexión a MySQL
    - Sistema de usuarios con login
    - Interfaz visual atractiva y adaptable

autor:
  nombre: Oscar David Pinzón Guio
  descripcion: Licenciado en música | Guitarrista | Estudiante de Ingeniería de Sistemas
  ubicacion: Zipaquirá, Colombia
