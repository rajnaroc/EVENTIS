from flask import Flask, app, flash, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL

# importaciones de los .py
from config import config
from forms import loginform, registerForm, perfilform
from entities.ModelUser import ModelUser

app = Flask(__name__)

db = MySQL(app)

login_manager = LoginManager(app)


# funcion para verificar si el usuario tiene la sesion iniciada
@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# funcion para mostrar la pagina de inicio
@app.route('/', methods=['GET'])
def inicio():
    return render_template('inicio.html')

# funcion para iniciar sesion
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

# funcion para registrar un nuevo usuario
@app.route('/registrarse', methods=['GET', 'POST'])
def register():
    register = registerForm()
    
    if request.method == 'POST':
        nombre = register.nombre.data
        correo = register.correo.data
        contraseña = register.contraseña.data
        fecha_nacimiento = register.fecha_nacimiento.data
        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            flash("Usuario registrado correctamente.")
            login_user(ModelUser.sesion(db, correo, contraseña))
            return render_template('inicio.html')
        else:
            return render_template('register.html', register=register)
    if request.method == 'GET':
        return render_template('register.html', register=register)


# funcion para mostrar el perfil y editarlo
@app.route('/perfil', methods=['GET','POST'], )
@login_required
def perfil():
    form=perfilform(obj=current_user)

    if request.method == "GET":
            return render_template('perfil.html',   form=form, user=current_user)
    
    if request.method == "POST":
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']

# funcion para actualizar el perfil
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required 
def editar_perfil():
    user = ModelUser.get_by_id(db, current_user.id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        if ModelUser.update_user(db, user.id, nombre, correo, contraseña, fecha_nacimiento):
            flash("Perfil actualizado correctamente.")
            return render_template('perfil.html', user=user)
        else:
            flash("Error al actualizar el perfil.")
    
    return render_template('editar_perfil.html', user=user)

# funcion para eliminar el perfil
@app.route('/perfil/eliminar', methods=['GET'])
@login_required
def eliminar_cuenta():
    user = ModelUser.get_by_id(db, current_user.id)
    if request.method == 'POST':
        ModelUser.delete_user(db, user.id)
        logout_user()
        flash("Perfil eliminado correctamente.")
        return render_template('inicio.html')
    
    return render_template('eliminar_perfil.html', user=user)

# funcion para cerrar sesion
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('inicio.html')

# funcion para mostrar el error 404
def status_404(error):
    return render_template('404.html')

if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.register_error_handler(404, status_404)
    app.run()