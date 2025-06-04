from flask import flash
from .models.User import User
from datetime import datetime

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
                cur.close()
                return user
            return None
        except Exception as e:
            print(e)
    
    # funcion para registrar un nuevo usuario y verificar si el correo ya existe
    @classmethod
    def register(cls, db, nombre, correo, contraseña, fecha_nacimiento):
        try:
            # Verificar si el correo ya existe
            cur = db.connection.cursor()

            # Hashear la contraseña
            hashed_password = User.hash_password(contraseña)
            
            print(hashed_password)
            # Insertar el nuevo usuario
            cur.execute(
                "INSERT INTO usuarios (id, nombre, correo, contraseña, fecha_nacimiento, saldo, fecha_registro) "
                "VALUES (NULL, %s, %s, %s, %s, 0, NOW())",
                (nombre, correo, hashed_password, fecha_nacimiento)
            )
            
            db.connection.commit()
            cur.close()

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
                    
                    cur.close()
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
                cur.close()
                return data
            
            cur.close()
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

            cur.close()
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
    
            
            return True
        except Exception as e:
            print(e)
            return False
        
    # funcion para crear un evento    
    @classmethod
    def crear_eventos(cls,db,titulo,descripcion,fecha,lugar,precio,categoria,aforo,hora_inicio,hora_fin):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "INSERT INTO eventos (titulo, descripcion, fecha, lugar,precio,categoria,aforo,hora_inicio,hora_fin) "
                "VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s)",
                (titulo,descripcion,fecha,lugar,precio,categoria,aforo,hora_inicio,hora_fin)
            )
            db.connection.commit()
            evento_id = cur.lastrowid
            
            cur.close()
            return evento_id
        except Exception as e:
            print(e)
            return False
    @classmethod
    def update_user(cls,db, id, nombre, correo,fecha_nacimiento):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE usuarios SET nombre = %s, correo = %s, fecha_nacimiento = %s WHERE id = %s",(nombre,correo,fecha_nacimiento,id))
            db.commit
            cur.close()

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
            cur.close()
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
            cur.execute(" SELECT titulo, descripcion, fecha, lugar, precio, categoria, aforo,hora_inicio,hora_fin FROM eventos WHERE id = %s", (id,))


            data = cur.fetchone() 
            cur.close()

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
                cur.close()
                return True
            
            cur.close()
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
                cur.close()
                return data
            
            cur.close()
            return None
        
        except Exception as e:
            print(e)
            return None
        
    # funcion para ver los eventos con sus fotos
    @classmethod
    def evento(cls, db):
        try:
            cur = db.connection.cursor()
            cur.execute("""
                SELECT 
                    e.id, e.titulo, e.descripcion, e.fecha, e.lugar, e.precio, e.aforo, e.categoria, DATE_FORMAT(e.hora_inicio, '%H:%i') AS hora_inicio,DATE_FORMAT(e.hora_fin, '%H:%i') AS hora_fin,
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
            cur.close()

            return eventos
        except Exception as e:
            print(e)
            return None

    # obtener las fotos de un evento por id
    @classmethod
    def obtener_fotos_evento(cls, db, id):
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT id,ruta,public_id FROM fotos_evento WHERE id_evento = %s", (id,))
            fotos = cur.fetchall()

            cur.close()
            return fotos
            
        except Exception as e:
            print(e)
            return None
        
    # carrusel del inicio de imagenes
    @classmethod
    def carrusel_img(cls,db):
        try:
            cur = db.connection.cursor()
            
            cur.execute("SELECT ruta FROM fotos_evento ORDER BY id DESC")
            
            imagenes = [fila[0] for fila in cur.fetchall()]
            
            cur.close()
            return imagenes
        
        except Exception as e:
            print(e)
            return []
    # funcion para editar un evento
    @classmethod
    def editar_evento(cls, db, id, titulo, descripcion, fecha, lugar, precio, categoria, aforo, hora_inicio,hora_fin):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "UPDATE eventos SET titulo = %s, descripcion = %s, fecha = %s, lugar = %s, precio = %s, categoria = %s, aforo = %s, hora_inicio = %s, hora_fin = %s WHERE id = %s",
                (titulo, descripcion, fecha, lugar, precio, categoria, aforo,hora_inicio,hora_fin, id)
            )
            db.connection.commit()
            cur.close()
    
            return True
        except Exception as e:
            print(e)
            return False
    @classmethod
    def historial_compras(cls,db,usuario_id):
        try:
            cur = db.connection.cursor()
            cur.execute("""
                SELECT 
                    e.id AS entrada_id,e.usuario_id,e.evento_id,e.precio,e.fecha_compra,e.estado,
                    ev.titulo,ev.descripcion,ev.fecha AS fecha_evento,ev.hora_inicio,ev.hora_fin,ev.lugar,ev.categoria
                FROM entradas e
                JOIN eventos ev ON e.evento_id = ev.id
                WHERE e.usuario_id = %s
                ORDER BY e.fecha_compra DESC
            """, (usuario_id,))

            entradas = cur.fetchall()
            cur.close()
            return entradas

        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def procesar_devolucion(cls, db, entrada_id, usuario_id):
        try:
            cur = db.connection.cursor()

            # Obtener datos
            cur.execute("""
                SELECT e.id, e.estado, ev.fecha,ev.id
                FROM entradas e
                JOIN eventos ev ON e.evento_id = ev.id
                WHERE e.id = %s AND e.usuario_id = %s
            """, (entrada_id, usuario_id))
            entrada = cur.fetchone()

            if not entrada:
                flash("No se encontró la entrada para este usuario","info")
                cur.close()
                return False

            estado = entrada[1]
            fecha_evento = entrada[2]

            # Convertir fecha_evento a datetime.date si viene como string
            if isinstance(fecha_evento, str):
                fecha_evento = datetime.strptime(fecha_evento, '%Y-%m-%d').date()

            hoy = datetime.now().date()
            diferencia = (fecha_evento - hoy).days
            

            # Condiciones para devolución
            if estado.lower() != "comprada":
                flash("Estado incorrecto para devolución: {}".format(estado),"error")
                cur.close()
                return False

            if diferencia < 2:
                flash("No se puede devolver, el evento es en {} días {}".format(diferencia,2),"error")
                cur.close()
                return False

            # Actualizar estado
            cur.execute("""
                UPDATE entradas SET estado = 'reembolsado' WHERE id = %s
            """, (entrada_id,))

            cur.execute("""
                UPDATE eventos SET aforo = aforo + 1 WHERE id = %s
            """, (entrada[3],))

            db.connection.commit()
            cur.close()
            return True

        except Exception as e:
            print("Error en devolución:", e)
            return False


    @classmethod
    def restar_entradas(cls,db, evento_id, cantidad):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE eventos SET aforo = aforo - %s WHERE id = %s AND aforo >= %s", (cantidad, evento_id, cantidad))
            db.connection.commit()
            cur.close()
            return cur.rowcount > 0  
        
        except Exception as e:
            db.connection.rollback()
            print("Error al restar entradas:", e)
            return False
    
    @classmethod
    def obtener_fotos_con_categorias(cls, db):
        try:
            cur = db.connection.cursor()
            cur.execute("""
                SELECT e.categoria,f.ruta
                FROM fotos_evento f
                JOIN eventos e ON f.id_evento = e.id
            """)
            
            resultados = cur.fetchall()
            cur.close()

            return resultados
        except Exception as e:
            print(e)
            return []

    