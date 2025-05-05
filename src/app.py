from flask import Flask, app, render_template, request
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
# importaciones de los .py
from config import config
from forms import loginform, registerForm
from entities import ModelUser

app = Flask(__name__)
db = MySQL(app)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/iniciarsesion', methods=['GET'])
def iniciar_sesion():
    login = loginform()
    if request.method == 'POST':
        pass
    if request.method == "GET":
        return render_template('iniciar_sesion.html', login=login)

@app.route('/registrarse', methods=['GET'])
def register():
    register = registerForm()
    return render_template('register.html', register=register)

def status_404(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.register_error_handler(404, status_404)
    app.run()