from flask import flash
from .models.User import User

class ModelUser:

    # funcion para revisar si tiene la sesion iniciada
    @classmethod
    def get_by_id(cls,db,id):
        try: 

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            data = cur.fetchone()

            if data:
                id = data[0]
                nombre = data[1]
                correo = data[2]
                contraseña = None
                fecha_nacimiento = data[4]
                saldo = data[5]
                # Crear una instancia de User y devolverla
                user = User(id,nombre,correo,contraseña,fecha_nacimiento,saldo)

                return user
            return None
        except Exception as e:
            print(e)
    
    # funcion para registrar un nuevo usuario y verificar si el correo ya existe
    @classmethod
    def register(cls, db, nombre, correo, contraseña, fecha_nacimiento):
        try:
            # Verificar si el correo ya existe
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            
            print(cursor.fetchone())

            if cursor.fetchone():
                flash("El correo ya está registrado.")
                return False

            # Hashear la contraseña
            hashed_password = User.hash_password(contraseña)
            
            print(hashed_password)
            # Insertar el nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (id, nombre, correo, contraseña, fecha_nacimiento, saldo, fecha_registro) "
                "VALUES (NULL, %s, %s, %s, %s, 0, NOW())",
                (nombre, correo, hashed_password, fecha_nacimiento)
            )
            
            db.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            print(e)
            return False
    
    # funcion para iniciar sesion y verificar si el usuario existe
    @classmethod
    def sesion(cls,db,correo,contraseña):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            data = cur.fetchone()

            if data:
                id = data[0]
                nombre = data[1]
                correo = data[2]
                hashed_contraseña = data[3]
                fecha_nacimiento = data[4]
                saldo = data[5]

                valor = User.check_password(hashed_contraseña,contraseña)
                User.check_password(hashed_contraseña,contraseña)
                print(valor)
                if valor:
                    # Si la contraseña es correcta, crea una instancia de User y devuelve el objeto
                    user = User(id,nombre,correo,None,fecha_nacimiento,saldo)

                    return user
                
                return flash("error password")
            
        except Exception as e:
            print(e)
    
    # funcion para ver el historial de compras del usuario
    @classmethod
    def historial_compras(cls,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM compras WHERE usuario_id = %s", (id,))
            data = cur.fetchall()

            if data:
                return data
            
            return None
        except Exception as e:
            print(e)

    @classmethod
    def contacto(cls,db,usuario_id, nombre, correo, mensaje):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "INSERT INTO mensajes_contacto (id, usuario_id, nombre, correo, mensaje) "
                "VALUES (NULL, %s, %s, %s, %s)",
                (usuario_id,nombre, correo, mensaje)
            )
            db.connection.commit()
            cur.close()
            flash("Mensaje enviado correctamente.")

            return True
        except Exception as e:
            print(e)
            return False
    
    # funcion para borrar el usuario de la base de datos
    @classmethod
    def delete_user(cls,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            db.connection.commit()
            cur.close()
            flash("Usuario eliminado correctamente.")   
            return True
        except Exception as e:
            print(e)
            return False
        
    