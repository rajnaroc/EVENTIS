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
        if form.validate_on_submit():
            # recoger los valores del input
            nombre = request.form['nombre']
            correo = request.form['correo']
            mensaje = request.form['mensaje']
            # funcion para mandar el mensaje a la pagina
            if ModelUser.contacto(db,current_user.id, nombre, correo, mensaje):
                flash("Mensaje enviado correctamente.","success")
                return redirect(url_for('contacto.contacto'))
            flash("Error al mandar el mensaje","error")
            return redirect(url_for('contacto.contacto')) 
        else:
            flash("Dato no valido en los inputs","error")
            return redirect(url_for('contacto.contacto')) 
        
@contacto_bp.route('/contacto/admin', methods=['GET', 'POST'])
def contacto_admin():

    if request.method == 'GET':
        mensajes = ModelUser.mensajes(db)
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            return render_template('admin_mensajes.html', mensajes=mensajes )
        else:
            return redirect(url_for('auth.iniciar_sesion'))
        

@contacto_bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_mensaje(id):
    if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
        ModelUser.delete_mensaje(db, id)
        flash('Mensaje eliminado correctamente.', 'success')
        return redirect(url_for('contacto.contacto_admin'))
    
    return redirect(url_for('auth.iniciar_sesion'))