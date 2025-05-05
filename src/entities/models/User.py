from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash

class User(UserMixin):
    
    def __init__(self,id,nombre,correo,contraseña,fecha_nacimiento,saldo):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.fecha_nacimiento = fecha_nacimiento
        self.saldo = saldo

    @classmethod
    def check_password(cls,segura_contraseña,contraseña):
        return check_password_hash(segura_contraseña,contraseña)
    
    @classmethod
    def hash_password(cls,contraseña):
        return generate_password_hash(contraseña)