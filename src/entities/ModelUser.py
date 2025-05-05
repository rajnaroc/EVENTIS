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
                
                user = User(id,nombre,correo,contraseña,fecha_nacimiento)

                return user
            return None
        except Exception as e:
            print(e)
    @classmethod
    def register(cls, db, nombre, correo, contraseña, fecha_nacimiento):
        try:
            User(nombre, correo, contraseña, fecha_nacimiento)
            cursor = db.connection.cursor()
            hashed_password = User.hash_password(contraseña)  
            cursor.execute("INSERT INTO users (id, nombre, correo, contraseña,fecha_nacimiento) VALUES (NULL, %s, %s, %s)", (nombre, correo, hashed_password,fecha_nacimiento))
            
            db.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            print(e)
    