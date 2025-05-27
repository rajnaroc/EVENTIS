from flask_mail import Mail, Message
from flask import Flask, app, flash, redirect, render_template, request, url_for
from flask_login import LoginManager,login_user, logout_user, current_user
from flask_mysqldb import MySQL
import cloudinary
import cloudinary.uploader
# importaciones de los .py
from config import config
from forms import loginform, registerForm, perfilform,contactoform,crearEventoForm
from entities.ModelUser import ModelUser
from utils.email_sender import enviar_correo_bienvenida, plantilla_bienvenida

app = Flask(__name__)

app.config.from_object(config['dev']) 


db = MySQL(app)

mail = Mail(app)


login_manager = LoginManager(app)

# funcion para verificar si el usuario tiene la sesion iniciada
@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

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

            evento_id = ModelUser.crear_eventos(db,titulo,descripcion,fecha,lugar,precio,categoria,aforo)
            
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
            eventos = ModelUser.evento_solo(db, id)
            columnas = ['titulo', 'descripcion', 'fecha', 'hora', 'lugar', 'precio', 'categoria', 'aforo']
            print(eventos)
            fotos = ModelUser.obtener_fotos_evento(db, id)
            valores = zip(columnas, eventos)
            categorias = {
                1: 'Concierto',
                2: 'Teatro',
                3: 'Deporte',
                4: 'Cine',
                5: 'Otros'
            }
            evento = crearEventoForm(data=valores)

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

            evento_id = ModelUser.editar_evento( db, id, titulo, descripcion, fecha, lugar, precio, categoria, aforo)
            
            # Guardar cada imagen en la tabla imagenes_evento
            for url in urls_imagenes:
                ModelUser.editar_fotos_evento(db, evento_id, url)
            flash("Evento editado correctamente.")

            return redirect(url_for('eventos_admin'))
        else:
            return redirect(url_for('inicio'))

@app.route('/evento/<int:evento_id>')
def detalle_evento(evento_id):
    if current_user.is_authenticated:
        evento = ModelUser.obtener_evento_detalle(db,evento_id)
        foto = ModelUser.obtener_fotos_evento(db, evento_id)
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

# funcion para mostrar el error 404
def status_404(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.register_error_handler(404, status_404)
    app.run()