#!/usr/bin/env python3
"""
Script de instalación para la Tienda Online
Este script ayuda a configurar la aplicación automáticamente
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def install_requirements():
    """Instala las dependencias de Python"""
    print("📦 Instalando dependencias de Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def test_mysql_connection(host, user, password, database):
    """Prueba la conexión a MySQL"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("✅ Conexión a MySQL exitosa")
            connection.close()
            return True
    except Error as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        return False
    return False

def create_database(host, user, password, database_name):
    """Crea la base de datos si no existe"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✅ Base de datos '{database_name}' creada/verificada")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error al crear base de datos: {e}")
        return False

def update_app_config(host, user, password, database):
    """Actualiza la configuración en app.py"""
    config_line = f"app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{host}/{database}'"
    
    try:
        with open('app.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Buscar y reemplazar la línea de configuración
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "SQLALCHEMY_DATABASE_URI" in line and "mysql://" in line:
                lines[i] = f"app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{user}:{password}@{host}/{database}'"
                break
        
        with open('app.py', 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))
        
        print("✅ Configuración actualizada en app.py")
        return True
    except Exception as e:
        print(f"❌ Error al actualizar configuración: {e}")
        return False

def main():
    print("🏪 Instalador de Tienda Online")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ No se encontró app.py. Ejecuta este script desde el directorio del proyecto.")
        return
    
    # Instalar dependencias
    if not install_requirements():
        return
    
    print("\n🔧 Configuración de Base de Datos")
    print("-" * 30)
    
    # Solicitar información de la base de datos
    host = input("Host de MySQL (localhost): ").strip() or "localhost"
    user = input("Usuario de MySQL (root): ").strip() or "root"
    password = input("Contraseña de MySQL: ").strip()
    database = input("Nombre de la base de datos (tienda_online): ").strip() or "tienda_online"
    
    # Crear base de datos
    if not create_database(host, user, password, database):
        return
    
    # Probar conexión
    if not test_mysql_connection(host, user, password, database):
        return
    
    # Actualizar configuración
    if not update_app_config(host, user, password, database):
        return
    
    print("\n🎉 ¡Instalación completada!")
    print("=" * 40)
    print("Para iniciar la aplicación:")
    print("  python app.py")
    print("\nAccede a:")
    print("  Frontend: http://localhost:5000")
    print("  Admin: http://localhost:5000/admin")
    print("\nUsuario administrador:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")

if __name__ == "__main__":
    main()
