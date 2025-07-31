import mysql.connector
from mysql.connector import Error
from database import create_connection
from Models import *
from Services import *

def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n--- SISTEMA DE GESTIÓN DE HORARIOS ---")
    print("1. Crear nueva clase para sección")
    print("2. Asignar recursos a clase existente")
    print("3. Generar horario por sección")
    print("4. Salir del sistema")

def main():
    """Función principal del sistema"""
    conn = create_connection()
    if conn is None:
        return
    
    try:
        while True:
            mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                crear_nueva_clase(conn)
            elif opcion == "2":
                asignar_recursos_clase(conn)
            elif opcion == "3":
                generar_horario(conn)
            elif opcion == "4":
                print("\n¡Gracias por usar el Sistema de Gestión de Horarios!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()