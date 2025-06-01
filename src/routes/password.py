from extension.extesion import *

pass_bp = Blueprint('pass', __name__)

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

def generar_token_correo(correo):
    return serializer.dumps(correo, salt="recuperar-clave")


def verificar_token(token, max_age=600):  # 600 segundos = 10 minutos
    try:
        correo = serializer.loads(token, salt="recuperar-clave", max_age=max_age)
        return correo
    except Exception:
        return None


@pass_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['correo']
        
        cur = db.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE correo=%s", (correo,))
        user = cur.fetchone()

        if user:
            token = generar_token_correo(correo)
            enlace = url_for('pass.cambiar_contraseña', token=token, _external=True)
            # Enviar correo
            mensaje = Message("Recuperación de contraseña",sender='aaroncm611@gmail.com',recipients=[correo])
            mensaje.body = f"""
                Hola,

                Recibimos una solicitud para restablecer tu contraseña.
                Haz clic en este enlace para cambiarla (expira en 10 minutos):

                {enlace}

                Si no fuiste tú, ignora este mensaje.
                """
            mail.send(mensaje)

            flash("Se ha enviado un enlace a tu correo", "success")
            return redirect(url_for("pass.recuperar"))
        else:
            flash("Correo no registrado", "error")

    if request.method == "GET": 
        return render_template("recuperar.html",form=perfilform())


@pass_bp.route('/cambiar/<token>', methods=['GET', 'POST'])
def cambiar_contraseña(token):
    
    correo = verificar_token(token)

    if not correo:
        flash("El enlace ha expirado o no es válido", "error")
        return redirect(url_for('auth.iniciar_sesion'))

    form = CambiarContraseñaForm()

    if request.method == 'POST':
        nueva = request.form['password']
        hash = generate_password_hash(nueva)

        cur = db.connection.cursor()
        cur.execute("UPDATE usuarios SET contraseña=%s WHERE correo=%s", (hash, correo))
        db.connection.commit()

        flash("Contraseña cambiada correctamente", "success")
        return redirect(url_for("auth.iniciar_sesion"))
    
    return render_template("cambiar.html",form=form)

