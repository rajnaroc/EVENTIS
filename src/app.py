from math import log
from flask import Flask, app, render_template
from config import config
from forms import loginform, registerForm

app = Flask(__name__)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/iniciarsesion', methods=['GET'])
def iniciar_sesion():
    login = loginform()
    return render_template('iniciar_sesion.html', login=login)

@app.route('/registrarse', methods=['GET'])
def register():
    register = registerForm()
    return render_template('register.html', register=register)

if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.run()