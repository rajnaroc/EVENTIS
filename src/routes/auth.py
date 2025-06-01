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
            return render_template('inicio.html')
        else:
            return render_template('iniciar_sesion.html', login=login, error="Usuario o contraseña incorrectos")
    
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('general.inicio'))
        else:
            return render_template('iniciar_sesion.html', login=login)
        
# funcion para registrar un nuevo usuario(usuario)
@auth_bp.route('/registrarse', methods=['GET', 'POST'])
def register():
    register = registerForm()
    
    if request.method == 'POST':

        # recoger los valores del input
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']

        # Verificar si el correo ya está registrado
        if ModelUser.exists(db, correo):
            flash("El correo ya está registrado. Por favor, inicia sesión o utiliza otro correo.","error")
            return redirect(url_for('auth.register'))
        
        # funcion para registar al usuario 
        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            flash("Registrado correctamente","success")
            
            # Enviar correo de bienvenida
            enviar_correo_bienvenida(Message, mail, correo, plantilla_bienvenida(nombre))
            
            # iniciar sesion automaticamente al registrarse
            login_user(ModelUser.sesion(db, correo, contraseña))
            
            flash("Bienvenido {} usuario".format(nombre),"success")
            return redirect(url_for('general.inicio'))
        else:
            flash
            return redirect(url_for('register.html'))
    
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('inicio'))
        else:
            return render_template('register.html', register=register)

# funcion para cerrar la sesion(usuario)
@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("Cerrada la sesion","info")
    return redirect(url_for('general.inicio'))
