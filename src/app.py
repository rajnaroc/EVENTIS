import re
from flask import Flask, app, flash, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from utils.email_sender import enviar_correo, plantilla_bienvenida
# importaciones de los .py
from config import config
from forms import loginform, registerForm, perfilform,contactoform,crearEventoForm
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
        if current_user.is_authenticated:
            return redirect(url_for('inicio'))
        else:
            return render_template('iniciar_sesion.html', login=login)

# funcion para registrar un nuevo usuario
@app.route('/registrarse', methods=['GET', 'POST'])
def register():
    register = registerForm()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']

        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            flash("Usuario registrado correctamente.")
            # Enviar correo de bienvenida
            contenido_html = plantilla_bienvenida(nombre)
            enviar_correo(correo, "Bienvenido a Eventis", contenido_html)
            login_user(ModelUser.sesion(db, correo, contraseña))
            return render_template('inicio.html')
        else:
            return render_template('register.html', register=register)
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('inicio'))
        else:
            return render_template('register.html', register=register)


# funcion para mostrar el perfil y editarlo
@app.route('/perfil', methods=['GET','POST'], )
def perfil():
    form=perfilform(obj=current_user)

    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template('perfil.html',   form=form, user=current_user)
        else:
            return redirect(url_for('iniciar_sesion'))
    if request.method == "POST":
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']

# funcion para actualizar el perfil
@app.route('/perfil/editar', methods=['GET', 'POST']) 
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

@app.route('/admin/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    form = crearEventoForm
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        hora = request.form['hora']
        lugar = request.form['lugar']
        imagen = request.form['imagen']
        # Guardar el evento en la base de datos
        ModelUser.crear_evento(db, titulo, descripcion, fecha, hora, lugar, imagen)
        flash('Evento creado correctamente')
        return redirect(url_for('crear_evento'))
    if request.method == 'GET':
        return render_template('admin_crear_evento.html', form=form)



# funcion para ver los mensajes del usuario
@app.route('/perfil/mensajes', methods=['GET'])
def mensajes():
    if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
        mensajes = ModelUser.mensajes(db)
        return render_template('admin_mensajes.html', mensajes=mensajes)
    else:
        return redirect(url_for('iniciar_sesion'))
    

# funcion para eliminar el mensaje de contacto
@app.route('/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar_mensaje(id):
    if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
        ModelUser.delete_mensaje(db, id)
        flash("Mensaje eliminado correctamente.")
        return redirect(url_for('mensajes'))
    else:
        return redirect(url_for('iniciar_sesion'))


# funcion para eliminar el perfil
@app.route('/perfil/eliminar', methods=['POST', 'GET'])
def eliminar_cuenta():
    user = ModelUser.get_by_id(db, current_user.id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            ModelUser.delete_user(db, user.id)
            logout_user()
            flash("Perfil eliminado correctamente.")
            return redirect(url_for('inicio.html'))

# funcion para mostrar el historial 
@app.route('/historial', methods=['GET'])
def historial_compras():
    if current_user.is_authenticated:
        compra = ModelUser.historial_compras(db, current_user.id)
        return render_template('historial_compras.html', compra=compra)
    else:
        return redirect(url_for('iniciar_sesion'))

# funcion para mostrar el contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = contactoform()

    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('contacto.html', form=form)
        else:
            return redirect(url_for('iniciar_sesion'))
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        if ModelUser.contacto(db,current_user.id, nombre, correo, mensaje):
            flash("Mensaje enviado correctamente.")
            return redirect(url_for('contacto'))

# funcion para cerrar sesion
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('inicio'))

# Ruta para mostrar el Aviso Legal
@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso_legal.html')

# Ruta para mostrar la Política de Privacidad
@app.route('/politica-privacidad')
def politica_privacidad():
    return render_template('politica_privacidad.html')

# Ruta para mostrar la Política de Cookies
@app.route('/terminoscondiciones')
def terminos_condiciones():
    return render_template('terminos_condiciones.html')

# funcion para mostrar el error 404
def status_404(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.config.from_object(config["dev"])
    app.register_error_handler(404, status_404)
    app.run()