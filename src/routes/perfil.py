from extension.extesion import *

perfil_bp = Blueprint('perfil', __name__)

# Funcion para ver el perfil(usuario)
@perfil_bp.route('/perfil')
def perfil():

    form=perfilform(obj=current_user)

    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template('perfil.html',   form=form, user=current_user)
        else:
            return redirect(url_for('iniciar_sesion'))
        
# Funcion para editar el perfil(admin)
@perfil_bp.route('/perfil/editar', methods=['GET', 'POST'])
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

# Funcion para eliminar la cuenta del usuario(usuario)
@perfil_bp.route('/eliminar', methods=['POST'])
def eliminar_cuenta():
    user = ModelUser.get_by_id(db, current_user.id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            ModelUser.delete_user(db, user.id)
            logout_user()
            flash("Perfil eliminado correctamente.")
            return redirect(url_for('inicio.html'))
        
@perfil_bp.route('/historial', methods=['GET'])
def historial_compras():
    if current_user.is_authenticated:
        compra = ModelUser.historial_compras(db, current_user.id)
        print(compra)
        return render_template('historial_compras.html', compra=compra)
    else:
        return redirect(url_for('iniciar_sesion'))