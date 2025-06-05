from extension.extesion import *
admin_bp = Blueprint('admin', __name__,)

@admin_bp.route('/admin/usuarios', methods=["GET"])
def admin_usuarios():
    
    if request.method == "GET" and current_user.correo == "aaroncm611@gmail.com":
        pagina = int(request.args.get('page', 1))
        por_pagina = 5
        usuarios, total_usuarios = ModelUser.obtener_usuarios_paginados(db, pagina, por_pagina)
        total_paginas = (total_usuarios + por_pagina - 1) // por_pagina
        
        return render_template('admin_usuarios.html', usuarios=usuarios, pagina=pagina, total_paginas=total_paginas)
    
    else:  
        return abort(404)

@admin_bp.route('/admin/usuarios/<int:usuario_id>')
def admin_usuario_detalle(usuario_id):
    if request.method == "GET" and current_user.correo == "aaroncm611@gmail.com":
        usuario = ModelUser.obtener_usuario_por_id(db, usuario_id)
        entradas = ModelUser.obtener_entradas_usuario(db, usuario_id)
        return render_template('admin_usuario_detalle.html', usuario=usuario, entradas=entradas)
    else:
        return abort(404)

@admin_bp.route('/admin/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
def admin_usuario_editar(usuario_id):
    
    if request.method == 'POST' and current_user.correo == "aaroncm611@gmail.com":
        
        nombre = request.form['nombre']
        correo = request.form['correo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        saldo = request.form['saldo']
        ModelUser.actualizar_usuario(db, usuario_id, nombre, correo, fecha_nacimiento, saldo)
        flash("Datos modificados con exito","success")
        return redirect(url_for('admin.admin_usuarios'))
    
    if request.method == "GET" and current_user.correo == "aaroncm611@gmail.com":
        usuario = ModelUser.obtener_usuario_por_id(db, usuario_id)
        flash("Editado con exito el usuario","success")
        return render_template('admin_usuario_editar.html', usuario=usuario)
    
    else:
        return abort(404)

@admin_bp.route('/admin/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def admin_usuario_eliminar(usuario_id):
    
    if request.method == 'POST' and current_user.correo == "aaroncm611@gmail.com":
        ModelUser.eliminar_usuario(db, usuario_id)
        flash("El usuario con el id {} fue eliminado".format(usuario_id),"success")
        return redirect(url_for('admin.admin_usuarios'))
    else:
        return abort(404)
