# funcion para mostrar la pagina de inicio
@app.route('/', methods=['GET'])
def inicio():
    cursor = db.connection.cursor()
    cursor.execute("SELECT ruta FROM fotos_evento ORDER BY id DESC")
    imagenes = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    return render_template('inicio.html',imagenes=imagenes)


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
        print(compra)
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

# funcion para mostrar el evento
@app.route('/eventos/admin', methods=['GET', 'POST'])
def eventos_admin():
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


            return redirect(url_for('eventos_admin'))
        else:
            return redirect(url_for('inicio'))
        
# funcion para mostrar el eventos
@app.route('/eventos', methods=['GET'])
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
        return redirect(url_for('iniciar_sesion'))

# funcion para enseñar eventos
@app.route('/eventos/editar', methods=['GET', 'POST'])
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

# funcion para editar el evento que quieras tu
@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
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
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%d-%m-%Y').date()

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

            return redirect(url_for('eventos_admin'))
        else:
            return redirect(url_for('inicio'))

# pagina para ver la informacion general de evento
@app.route('/evento/<int:id>')
def detalle_evento(id):
    if current_user.is_authenticated:
        evento = ModelUser.obtener_evento_detalle(db,id)
        foto = ModelUser.obtener_fotos_evento(db, id)
        categorias = {
            1: 'Concierto',
            2: 'Teatro',
            3: 'Deporte',
            4: 'Cine',
            5: 'Otros'
        }
        if not evento:
            status_404(404)
        return render_template("evento.html", evento=evento, foto=foto, categorias=categorias)
    
    else:
        return redirect(url_for('iniciar_sesion'))
    
@app.route('/comprar/<int:evento_id>/<int:cantidad>', methods=['GET'])
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

    return redirect(url_for('detalle_evento', id=evento_id))




#function para eliminar el evento
@app.route('/eliminar_evento/<int:id>', methods=['POST', 'GET'])
def eliminar_evento(id):
    if current_user.is_authenticated and current_user.correo ==  "aaroncm611@gmail.com":
        ModelUser.delete_evento(db, id)
        flash("Evento eliminado correctamente.")
        return redirect(url_for('editar_eventos'))

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