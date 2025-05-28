from re import U
from extension.extesion import *


eventos_bp = Blueprint('eventos', __name__)

# Funcion para poder crear eventos(usuario)
@eventos_bp.route('/eventos/admin', methods=['GET', 'POST'])
def crear_evento():
    eventos = crearEventoForm()
    if request.method == 'GET':
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            return render_template('crear_eventos.html', form=eventos)
        else:
            return redirect(url_for('inicio'))
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fecha = request.form['fecha']
            lugar = request.form['lugar']
            precio = request.form['precio']
            categoria = request.form['categoria']
            aforo = request.form['aforo']
            hora_inicio = request.form['hora_inicio']
            hora_fin = request.form['hora_fin']
            
            imagenes = request.files.getlist('fotos')
            
            urls_imagenes = []
            
            for imagen in imagenes:
                if imagen.filename != '':
                    try:
                        # Subir a Cloudinary
                        resultado = cloudinary.uploader.upload(
                            imagen,
                            folder="eventos/",
                            resource_type="image"
                        )
                        urls_imagenes.append(resultado['secure_url'])
                    except Exception as e:
                        print(f"Error al subir imagen: {e}")

            evento_id = ModelUser.crear_eventos(db,titulo,descripcion,fecha,lugar,precio,categoria,aforo,hora_inicio,hora_fin)
            
            # Guardar cada imagen en la tabla imagenes_evento
            cursor = db.connection.cursor()
            for url in urls_imagenes:
                cursor.execute("INSERT INTO fotos_evento (id_evento, ruta) VALUES (%s, %s)", (evento_id, url))
            db.connection.commit()
            cursor.close()

# Funcion para enseñar los eventos del usuario(usuario)
@eventos_bp.route('/evento/<int:id>', methods=['GET'])
def evento_detalle(id):
    if request.method == "GET":
        if current_user.is_authenticated:
            evento = ModelUser.obtener_evento_detalle(db,id)
            foto = ModelUser.obtener_fotos_evento(db,evento[0])
            if request.method == "GET":
                categorias = {
                            1: 'Concierto',
                            2: 'Teatro',
                            3: 'Deporte',
                            4: 'Cine',
                            5: 'Otros'
                }
                print(evento)
                return render_template('evento.html', evento=evento,categorias=categorias,foto=foto)
        else:
            return redirect(url_for("auth.iniciar_sesion"))


# funcion para mostrar el eventos
@eventos_bp.route("/eventos", methods=['GET'])
def evento():
    if current_user.is_authenticated:
        eventos = ModelUser.eventos(db)
        categorias = {
            1: 'Concierto',
            2: 'Teatro',
            3: 'Deporte',
            4: 'Cine',
            5: 'Otros'
        }
        print(eventos)
        return render_template('eventos.html', eventos=eventos, categorias=categorias)
    else:
        return redirect(url_for('auth.iniciar_sesion'))


# funcion para enseñar los eventos a editar
@eventos_bp.route('/eventos/editar', methods=['GET', 'POST'])
def editar_eventos():
    if request.method == 'GET':
        
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            categorias = {
                1: 'Concierto',
                2: 'Teatro',
                3: 'Deporte',
                4: 'Cine',
                5: 'Otros'
            }
            eventos = ModelUser.eventos(db)
            return render_template('editar_eventos.html', eventos=eventos, categorias=categorias)
    return redirect(url_for('general.inicio'))

# Funcion para editar el evento por id y enseñar todos los eventos(admin)
@eventos_bp.route('/editar/Evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):

    if request.method == 'GET':
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            evento = ModelUser.evento_solo(db, id)
            fotos = ModelUser.obtener_fotos_evento(db, id)
            categorias = {
                1: 'Concierto',
                2: 'Teatro',
                3: 'Deporte',
                4: 'Cine',
                5: 'Otros'
            }
            
            fecha = evento[2]


            evento = crearEventoForm(data={
                'titulo': evento[0],
                'descripcion': evento[1],
                'fecha': fecha,
                'lugar': evento[3],
                'precio': evento[4],
                'categoria': evento[5],  
                'aforo': evento[6],      
                'hora_inicio': evento[7],
                'hora_fin': evento[8],
            })


            return render_template('panel_editar.html', form=evento, categorias=categorias, fotos=fotos)
    
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fecha = request.form['fecha']
            lugar = request.form['lugar']
            precio = request.form['precio']
            categoria = request.form['categoria']
            aforo = request.form['aforo']
            imagenes = request.files.getlist('fotos')
            hora_inicio = request.form['hora_inicio']
            hora_fin = request.form['hora_fin']
            
            urls_imagenes = []
            
            for imagen in imagenes:
                if imagen.filename != '':
                    try:
                        # Subir a Cloudinary
                        resultado = cloudinary.uploader.upload(
                            imagen,
                            folder="eventos/",
                            resource_type="image"
                        )
                        urls_imagenes.append(resultado['secure_url'])
                    except Exception as e:
                        print(f"Error al subir imagen: {e}")

            evento_id = ModelUser.editar_evento( db, id, titulo, descripcion, fecha, lugar, precio, categoria, aforo,hora_inicio,hora_fin)
            
            # Guardar cada imagen en la tabla imagenes_evento
            for url in urls_imagenes:
                ModelUser.editar_fotos_evento(db, evento_id, url)
            flash("Evento editado correctamente.")

            return redirect(url_for('eventos.editar_eventos'))
        else:
            return redirect(url_for('general.inicio'))

# Funcion para borrarlo(admin)
@eventos_bp.route('/eliminarEvento/<int:id>', methods=['POST'])
def eliminar_evento(id):
    if current_user.is_authenticated and current_user.correo ==  "aaroncm611@gmail.com":
        ModelUser.delete_evento(db, id)
        flash("Evento eliminado correctamente.")
        return redirect(url_for('eventos.editar_eventos'))

# gestionar el qr que se manda al correo
@eventos_bp.route('/comprar/<int:evento_id>/<int:cantidad>', methods=['GET'])
def comprar_entrada(evento_id,cantidad):
    if not current_user.is_authenticated:
        return redirect(url_for('iniciar_sesion'))

    for _ in range(cantidad):
        exito = generar_y_enviar_entrada_qr(
            usuario_email=current_user.correo,
            usuario_id=current_user.id,
            evento_id=evento_id, 
            precio=0.00,  
            estado='gratis',  # o 'comprada'
            db=db,
            mail=mail,
            Message=Message
        )

    if exito:
        flash("Entrada generada y enviada por correo", "success")
    else:
        flash("Error al generar la entrada", "danger")

    return redirect(url_for('eventos.evento_detalle', id=evento_id))
