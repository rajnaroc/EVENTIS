from calendar import c
from .models.User import User

class ModelUser:

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