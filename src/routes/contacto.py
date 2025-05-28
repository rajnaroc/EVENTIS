from extension.extesion import *


contacto_bp = Blueprint('contacto', __name__)


# Funcion para el formulario de contacto(usuario)
@contacto_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = contactoform()

    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('contacto.html', form=form)
        else:
            return redirect(url_for('auth.iniciar_sesion'))
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']
        if ModelUser.contacto(db,current_user.id, nombre, correo, mensaje):
            flash("Mensaje enviado correctamente.")
            return redirect(url_for('contacto'))