import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crea y retorna una conexión a la base de datos"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='0000',
            database='gestion_horarios'
        )
    except Error as e:
        print(f"Error al conectar a MariaDB: {e}")
        return None