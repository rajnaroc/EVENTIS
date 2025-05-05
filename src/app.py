from flask import Flask, app, render_template
from config import config


app = Flask(__name__)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

@app.route('/iniciarsesion', methods=['GET'])
def iniciar_sesion():
    return render_template('iniciar_sesion.html')

@app.route('/registrarse', methods=['GET'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.run()