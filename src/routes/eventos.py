from extension.extesion import *


eventos_bp = Blueprint('eventos', __name__)

# Funcion para poder crear eventos(admin)
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
            if eventos.validate_on_submit():
                # recoger los valores del input
                titulo = request.form['titulo']
                descripcion = request.form['descripcion']
                fecha = request.form['fecha']
                lugar = request.form['lugar']
                precio = request.form['precio']
                categoria = request.form['categoria']
                aforo = request.form['aforo']
                hora_inicio = request.form['hora_inicio']
                hora_fin = request.form['hora_fin']
                
                # coger las imagenes
                imagenes = request.files.getlist('fotos')
                
                urls_imagenes = []
                # hacemos un bucle para poder subirlas cloudinary

                for imagen in imagenes:
                    if imagen.filename != '':
                        try:
                            # Subir a Cloudinary
                            resultado = cloudinary.uploader.upload(
                                imagen,
                                folder="eventos/",
                                resource_type="image"
                            )
                            urls_imagenes.append({'url': resultado['secure_url'],'public_id': resultado['public_id']})
                        except Exception as e:
                            print("Error al subir imagen: {e}")

                # funcion para crear el evento y devolver el id 
                evento_id = ModelUser.crear_eventos(db,titulo,descripcion,fecha,lugar,precio,categoria,aforo,hora_inicio,hora_fin)
                
                # Guardar cada imagen en la tabla imagenes_evento
                cursor = db.connection.cursor()
                for url in urls_imagenes:
                    cursor.execute("INSERT INTO fotos_evento (id_evento, ruta,public_id) VALUES (%s, %s,%s)", (evento_id, url["url"],url["public_id"]))
                db.connection.commit()
                cursor.close()

                flash("Evento creado correctamente.","success") 
                return redirect(url_for('eventos.crear_evento'))
            flash("Error en el valor de un input.","error") 
            return redirect(url_for('eventos.crear_evento'))
            
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
                return render_template('evento.html', evento=evento,categorias=categorias,foto=foto)
        else:
            return redirect(url_for("auth.iniciar_sesion"))


# funcion para mostrar el eventos
@eventos_bp.route("/eventos", methods=['GET'])
def evento():
    if current_user.is_authenticated:
        eventos = ModelUser.evento(db)
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
@eventos_bp.route('/eventos/editar', methods=['GET'])
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
            # funcion para coger los eventos y enseñarlos en el panel
            eventos = ModelUser.eventos(db)
            return render_template('editar_eventos.html', eventos=eventos, categorias=categorias)
        return redirect(url_for('general.inicio'))

# Funcion para editar el evento por id y enseñar todos los eventos(admin)
@eventos_bp.route('/editar/evento/<int:id>', methods=['GET', 'POST'])
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
            
            # cargamos los datos del formulario para editarlos
            evento = crearEventoForm(data={
                'titulo': evento[0],
                'descripcion': evento[1],
                'fecha': evento[2],
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
            if evento.validate_on_submit():
                # recoger los valores del input
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

                # hacemos un bucle para poder subirlas cloudinary
                for imagen in imagenes:
                    if imagen.filename != '':
                        try:
                            # Subir a Cloudinary
                            resultado = cloudinary.uploader.upload(
                                imagen,
                                folder="eventos/",
                                resource_type="image"
                            )
                            urls_imagenes.append({'url': resultado['secure_url'],'public_id': resultado['public_id']})
                        except Exception as e:
                            print("Error al subir imagen: {e}")

                # funcion para crear el evento y devolver el id
                ModelUser.editar_evento( db, id, titulo, descripcion, fecha, lugar, precio, categoria, aforo,hora_inicio,hora_fin)
                
                cur = db.connection.cursor()
                cur.execute("SELECT id FROM eventos")
                evento_id = cur.fetchone()
                db.connection.commit()
                cur.close()

                # Guardar cada imagen en la tabla imagenes_evento
                cur = db.connection.cursor()
                for url in urls_imagenes:
                    cur.execute("INSERT INTO fotos_evento (id_evento, ruta,public_id) VALUES (%s, %s,%s)", (evento_id, url["url"],url["public_id"]))
                db.connection.commit()
                cur.close()
                flash("Evento editado correctamente.","success")
                return redirect(url_for('eventos.editar_eventos'))
            
            flash("Error en el valor de un input.","error") 
            return redirect(url_for('eventos.editar_eventos'))
        else:
            return redirect(url_for('general.inicio'))

# Funcion para borrarlo(admin)
@eventos_bp.route('/eliminarEvento/<int:id>', methods=["GET"])
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

    # cantidad de entradas que quiera una persona y se le manda al correo
    for _ in range(cantidad):
        exito = generar_y_enviar_entrada_qr(
            usuario_email=current_user.correo,
            usuario_id=current_user.id,
            evento_id=evento_id, 
            precio=0.00,  
            estado='gratis',
            db=db,
            mail=mail,
            Message=Message
        )
    ModelUser.restar_entradas(db, evento_id, cantidad)
    
    if exito:
        flash("Entrada generada y enviada por correo", "success")
    else:
        flash("Error al generar la entrada", "danger")

    return redirect(url_for('eventos.evento_detalle', id=evento_id))

@eventos_bp.route('/descargar_entrada/<int:entrada_id>')
def descargar_entrada(entrada_id):
    cur = db.connection.cursor()

    # Obtener datos de la entrada, el usuario y el evento
    cur.execute("""
        SELECT e.id, e.usuario_id, u.nombre, u.correo, e.evento_id, ev.titulo
        FROM entradas e
        JOIN usuarios u ON e.usuario_id = u.id
        JOIN eventos ev ON e.evento_id = ev.id
        WHERE e.id = %s
    """, (entrada_id,))
    
    entrada = cur.fetchone()
    cur.close()
    if not entrada:
        return "Entrada no encontrada", 404

    entrada_id, usuario_id, nombre_usuario, email, evento_id = entrada

    # Generar QR
    datos_qr = f"Entrada ID: {entrada_id}\nUsuario ID: {usuario_id}\nEvento ID: {evento_id}"
    qr_img = qrcode.make(datos_qr)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)

    # Crear PDF
    pdf_io = BytesIO()
    c = canvas.Canvas(pdf_io, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, 27 * cm, "Nombre: {}".format(nombre_usuario))
    c.drawString(2 * cm, 26 * cm, "Correo: {}".format(email))
    c.drawString(2 * cm, 25 * cm, "ID Entrada: {}".format(entrada_id))
    c.drawImage(qr_image, 2 * cm, 14 * cm, width=8 * cm, height=8 * cm)
    c.showPage()
    c.save()
    pdf_io.seek(0)

    return send_file(pdf_io, download_name=f'entrada_{entrada_id}.pdf', as_attachment=True)

@eventos_bp.route('/buscar', methods=["GET"])
def buscar_eventos():

    categoria = request.args.get('categoria')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    precio = request.args.get('precio')

    query = """
        SELECT  e.id,
                e.titulo,
                e.descripcion,
                e.fecha,
                e.lugar,
                e.precio,
                e.aforo, 
                e.categoria,
            (
                SELECT ruta 
                FROM fotos_evento f 
                WHERE f.id_evento = e.id 
                ORDER BY f.id ASC 
                LIMIT 1
            ) AS imagen
        FROM eventos e
        WHERE 1 = 1
    """
    params = []

    if categoria:
        query += " AND e.categoria = %s"
        params.append(categoria)

    if fecha_desde:
        query += " AND e.fecha >= %s"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND e.fecha <= %s"
        params.append(fecha_hasta)

    if precio == "gratis":
        query += " AND e.precio = 0"
    elif precio == "pago":
        query += " AND e.precio > 0"

    cur = db.connection.cursor()
    cur.execute(query, params)
    eventos = cur.fetchall()
    cur.close()
    print(eventos)

    categorias = {
        1: 'Concierto',
        2: 'Teatro',
        3: 'Deporte',
        4: 'Cine',
        5: 'Otros'
    }
    print(eventos)

    return render_template("eventos.html", eventos=eventos, categorias=categorias)

@eventos_bp.route('/eliminar_foto_evento/<int:id>/<path:public_id>/eliminar_foto_evento', methods=['GET'])
def eliminar_foto_evento(id,public_id):
    if current_user.is_authenticated and current_user.correo == "aaroncm611@gmail.com":

        public_id = unquote(public_id)

        try:
            cur = db.connection.cursor()
            cur.execute("DELETE FROM fotos_evento WHERE id = %s", (id,))
            db.connection.commit()
            cur.close()

            cloudinary.uploader.destroy(public_id)

            flash("Foto borrar con exito","success")

            return redirect(url_for('eventos.editar_eventos'))
        except Exception as e:
            print(e)
            return print('error Error al eliminar la foto')