from json import load
from webbrowser import get
from flask import Flask, app, render_template, request
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
# importaciones de los .py
from config import config
from forms import loginform, registerForm
from entities.ModelUser import ModelUser

app = Flask(__name__)

db = MySQL(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/iniciarsesion', methods=['GET', 'POST'])
def iniciar_sesion():
    login = loginform()
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        user = ModelUser.sesion(db, correo, contraseña)
        if user:
            login_user(user)
            return render_template('inicio.html')
        else:
            return render_template('iniciar_sesion.html', login=login, error="Usuario o contraseña incorrectos")
    
    if request.method == "GET":
        return render_template('iniciar_sesion.html', login=login)

@app.route('/registrarse', methods=['GET', 'POST'])
def register():
    register = registerForm()
    
    if request.method == 'POST':
        nombre = register.nombre.data
        correo = register.correo.data
        contraseña = register.contraseña.data
        fecha_nacimiento = register.fecha_nacimiento.data
        print(nombre, correo, contraseña, fecha_nacimiento)
        print(ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento))
        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            if ModelUser.sesion(db, correo, contraseña):
                print("Usuario registrado")
                return render_template('inicio.html')
        else:
            return render_template('register.html', register=register, error="El correo ya existe")
    if request.method == 'GET':
        return render_template('register.html', register=register)

def status_404(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.register_error_handler(404, status_404)
    app.run()