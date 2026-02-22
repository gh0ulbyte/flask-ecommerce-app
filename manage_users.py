#!/usr/bin/env python3
"""
Script para gestionar usuarios administradores
Uso: python manage_users.py [comando] [argumentos]
"""

import sys
import os
from werkzeug.security import generate_password_hash

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def create_admin(username, email, password):
    """Crear un nuevo usuario administrador"""
    with app.app_context():
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ El usuario '{username}' ya existe")
            return False
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"❌ El email '{email}' ya está registrado")
            return False
        
        # Crear nuevo usuario administrador
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"✅ Usuario administrador '{username}' creado exitosamente")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        return True

def list_users():
    """Listar todos los usuarios"""
    with app.app_context():
        users = User.query.all()
        print("\n📋 Lista de Usuarios:")
        print("-" * 60)
        print(f"{'ID':<3} {'Usuario':<15} {'Email':<25} {'Tipo':<12}")
        print("-" * 60)
        
        for user in users:
            user_type = "Admin" if user.is_admin else "Usuario"
            print(f"{user.id:<3} {user.username:<15} {user.email:<25} {user_type:<12}")
        
        print("-" * 60)
        print(f"Total: {len(users)} usuarios")

def toggle_admin(username):
    """Cambiar permisos de administrador de un usuario"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ Usuario '{username}' no encontrado")
            return False
        
        user.is_admin = not user.is_admin
        db.session.commit()
        
        status = "administrador" if user.is_admin else "usuario normal"
        print(f"✅ {username} ahora es {status}")
        return True

def show_help():
    """Mostrar ayuda"""
    print("""
🔧 Gestor de Usuarios - Tienda Online

Comandos disponibles:

1. Crear administrador:
   python manage_users.py create-admin [usuario] [email] [contraseña]
   
   Ejemplo:
   python manage_users.py create-admin juan juan@email.com mi_password123

2. Listar usuarios:
   python manage_users.py list

3. Cambiar permisos:
   python manage_users.py toggle [usuario]
   
   Ejemplo:
   python manage_users.py toggle juan

4. Ayuda:
   python manage_users.py help

Ejemplos de uso:
   python manage_users.py create-admin admin2 admin2@tienda.com admin456
   python manage_users.py list
   python manage_users.py toggle admin2
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "create-admin":
        if len(sys.argv) != 5:
            print("❌ Uso: python manage_users.py create-admin [usuario] [email] [contraseña]")
            return
        
        username = sys.argv[2]
        email = sys.argv[3]
        password = sys.argv[4]
        create_admin(username, email, password)
    
    elif command == "list":
        list_users()
    
    elif command == "toggle":
        if len(sys.argv) != 3:
            print("❌ Uso: python manage_users.py toggle [usuario]")
            return
        
        username = sys.argv[2]
        toggle_admin(username)
    
    elif command == "help":
        show_help()
    
    else:
        print(f"❌ Comando '{command}' no reconocido")
        show_help()

if __name__ == "__main__":
    main()
