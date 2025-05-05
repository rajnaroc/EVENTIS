from re import U
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
    
    # funcion para registrar un nuevo usuario y verificar si el correo ya existe
    @classmethod
    def register(cls, db, nombre, correo, contraseña, fecha_nacimiento):
        try:
            # Verificar si el correo ya existe
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            
            print(cursor.fetchone())
            if cursor.fetchone()!=None:
                print("Error: El correo ya está registrado.")
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
                
                return print("error password")
            
        except Exception as e:
            print(e)
