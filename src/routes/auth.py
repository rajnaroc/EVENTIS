from flask import session
from extension.extesion import *

auth_bp = Blueprint('auth', __name__)

# funcion para iniciar sesion el usuario(usuario)
@auth_bp.route('/iniciarsesion', methods=['GET', 'POST'])
def iniciar_sesion():
    
    login = loginform()
    
    if request.method == 'POST':
        
        # recoger los valores del input
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # funcion para iniciar sesion
        user = ModelUser.sesion(db, correo, contraseña)
        
        if user:
            login_user(user)
            session.permanent = True
            flash("Bienvenido {} usuario".format(user.nombre),"success")
            return redirect(url_for('general.inicio'))
        
        else:
            flash("Error en Iniciar sesion ")
            return render_template('iniciar_sesion.html', login=login)
    
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('general.inicio'))
        else:
            return render_template('iniciar_sesion.html', login=login)

@auth_bp.route('/registrarse', methods=['GET', 'POST'])
def register():
    form = registerForm()

    if current_user.is_authenticated:
        return redirect(url_for('general.inicio'))

    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        contraseña = form.contraseña.data
        fecha_nacimiento = form.fecha_nacimiento.data

        if ModelUser.exists(db, correo):
            flash("El correo ya está registrado. Por favor, inicia sesión o utiliza otro correo.", "error")
            return redirect(url_for('auth.register'))

        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            flash("Registrado correctamente", "success")

            enviar_correo_bienvenida(Message, mail, correo, plantilla_bienvenida(nombre))

            login_user(ModelUser.sesion(db, correo, contraseña))

            flash(f"Bienvenido {nombre} usuario", "success")
            return redirect(url_for('general.inicio'))
        else:
            flash("Error al registrar al usuario", "error")
            return redirect(url_for('auth.register'))

    # Si GET o si hubo errores
    return render_template('register.html', register=form)


# funcion para cerrar la sesion(usuario)
@auth_bp.route('/logout')
def logout():
    
    if current_user.is_authenticated:
        logout_user()
        flash("Cerrada la sesion","info")
        return redirect(url_for('general.inicio'))
    else:
        return redirect(url_for('general.inicio'))
