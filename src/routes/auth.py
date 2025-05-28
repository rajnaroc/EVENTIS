from extension.extesion import *

auth_bp = Blueprint('auth', __name__)

# funcion para iniciar sesion el usuario(usuario)
@auth_bp.route('/iniciarsesion', methods=['GET', 'POST'])
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
            return redirect(url_for('general.inicio'))
        else:
            return render_template('iniciar_sesion.html', login=login)
        
# funcion para registrar un nuevo usuario(usuario)
@auth_bp.route('/registrarse', methods=['GET', 'POST'])
def register():
    register = registerForm()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        fecha_nacimiento = request.form['fecha_nacimiento']
        # Verificar si el correo ya está registrado
        if ModelUser.exists(db, correo):
            flash("El correo ya está registrado. Por favor, inicia sesión o utiliza otro correo.")
            return render_template('register.html', register=register)
        if ModelUser.register(db, nombre, correo, contraseña, fecha_nacimiento):
            flash("Registrado correctamente")
            enviar_correo_bienvenida(Message, mail, correo, plantilla_bienvenida(nombre))
            # Enviar correo de bienvenida
            login_user(ModelUser.sesion(db, correo, contraseña))
            return render_template('inicio.html')
        else:
            return render_template('register.html', register=register)
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('inicio'))
        else:
            return render_template('register.html', register=register)

# funcion para cerrar la sesion(usuario)
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.inicio'))
