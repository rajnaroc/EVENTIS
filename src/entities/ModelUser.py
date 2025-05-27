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
        
    # funcion para ver los mensajes del usuario
    @classmethod
    def mensajes(cls,db):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM mensajes_contacto")
            data = cur.fetchall()
            print(data)
            return data
            
        except Exception as e:
            print(e)

    # funcion para eleminar el mensaje de contacto
    @classmethod
    def delete_mensaje(cls,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute("DELETE FROM mensajes_contacto WHERE id = %s", (id,))
            db.connection.commit()
            cur.close()
            flash("Mensaje eliminado correctamente.")   
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
        
    # funcion para crear un evento    
    @classmethod
    def crear_eventos(cls,db,titulo,descripcion,fecha,lugar,precio,categoria,aforo):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "INSERT INTO eventos (titulo, descripcion, fecha, lugar,precio,categoria,aforo) "
                "VALUES (%s, %s, %s, %s, %s, %s,%s)",
                (titulo,descripcion,fecha,lugar,precio,categoria,aforo)
            )
            db.connection.commit()
            evento_id = cur.lastrowid
            flash("Evento creado correctamente.")   
            cur.close()
            return evento_id
        except Exception as e:
            print(e)
            return False
    
    # funcion para ver los eventos
    @classmethod
    def eventos(cls,db):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM eventos")
            data = cur.fetchall()
            print(data)
            return data
            
        except Exception as e:
            print(e)
    
    # funcion para borrar el evento de la base de datos
    @classmethod
    def delete_evento(cls,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute("DELETE FROM eventos WHERE id = %s", (id,))
            db.connection.commit()
            cur.close()
            flash("Evento eliminado correctamente.")   
            return True
        except Exception as e:
            print(e)
            return False
    
    # funcion para ver un unico evento
    @classmethod
    def evento_solo(cls, db, id):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT titulo,descripcion,fecha,lugar,precio,categoria,aforo FROM eventos WHERE id = %s", (id,))
            data = cur.fetchone() 
            
            return data 
        except Exception as e:
            print(e)
            return None
    
    # funcion para comprobar si el usuario esta registrado ya
    @classmethod
    def exists(cls, db, correo):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            data = cur.fetchone()
            
            if data:
                return True
            
            return False
        except Exception as e:
            print(e)
            return False
    
    # funcion para ver evento por id
    @classmethod
    def obtener_evento_detalle(cls, db, id):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM eventos WHERE id = %s", (id,))
            data = cur.fetchone()
            
            if data:
                return data
            
            return None
        except Exception as e:
            print(e)
            return None
        
    # funcion para ver los eventos con sus fotos
    @classmethod
    def eventos(cls,db):
        try:
            cur = db.connection.cursor()
            cur.execute("""
                SELECT 
                    e.id, e.titulo, e.descripcion, e.fecha, e.lugar, e.precio, e.aforo, e.categoria,
                    (
                        SELECT ruta 
                        FROM fotos_evento f 
                        WHERE f.id_evento = e.id 
                        ORDER BY f.id ASC 
                        LIMIT 1
                    ) AS imagen
                FROM eventos e
            """)
            eventos = cur.fetchall()
            
            if eventos:
                return eventos
            
        except Exception as e:
            print(e)
            return None
    # obtener las fotos de un evento por id
    @classmethod
    def obtener_fotos_evento(cls, db, evento_id):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT ruta FROM fotos_evento WHERE id_evento = %s", (evento_id,))
            fotos = cur.fetchall()
            
            return fotos
            
        except Exception as e:
            print(e)
            return None
        
    # carrusel del inicio de imagenes
    @classmethod
    def carrusel_img(cls,db):
        try:
            cursor = db.connection.cursor()
            
            cursor.execute("SELECT ruta FROM fotos_evento ORDER BY id DESC")
            
            imagenes = [fila[0] for fila in cursor.fetchall()]
            
            return imagenes
        except Exception as e:
            print(e)
            return []
    # funcion para editar un evento
    @classmethod
    def editar_evento(cls, db, id, titulo, descripcion, fecha, lugar, precio, categoria, aforo):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "UPDATE eventos SET titulo = %s, descripcion = %s, fecha = %s, lugar = %s, precio = %s, categoria = %s, aforo = %s WHERE id = %s",
                (titulo, descripcion, fecha, lugar, precio, categoria, aforo, id)
            )
            db.connection.commit()
            cur.close()
            flash("Evento editado correctamente.")
            return True
        except Exception as e:
            print(e)
            return False
    # funcion para editar fotos de un evento
    @classmethod
    def editar_fotos_evento(cls, db, evento_id, fotos):
        try:
            cur = db.connection.cursor()
            # Eliminar fotos existentes
            cur.execute("DELETE FROM fotos_evento WHERE id_evento = %s", (evento_id,))
            
            # Insertar nuevas fotos
            for foto in fotos:
                cur.execute(
                    "INSERT INTO fotos_evento (id_evento, ruta) VALUES (%s, %s)",
                    (evento_id, foto)
                )
            
            db.connection.commit()
            cur.close()
            flash("Fotos del evento actualizadas correctamente.")
            return True
        except Exception as e:
            print(e)
            return False