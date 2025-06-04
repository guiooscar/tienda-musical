import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        port=3307,  
        user="root",
        password="",
        database="tienda_musical"
    )
