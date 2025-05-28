import os
import qrcode
from io import BytesIO
from datetime import datetime


def enviar_correo_bienvenida(Message,mail,destinatario, cuerpo):
    asunto = "¡Bienvenido a Eventis!"
    
    msg = Message(
        subject=asunto,
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[destinatario],
        html=cuerpo
    )

    
    try:
        mail.send(msg)
        return True
    
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False


# Plantilla de correo de bienvenida
def plantilla_bienvenida(nombre):
    return f"""
    <html>
    <body style="margin: 0; padding: 0; background-color: #121212; font-family: Arial, sans-serif; color: #f8f8f8;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: auto;">
            <tr>
                <td align="center" style="padding: 20px 0;">
                    <!-- Logo de la empresa -->
                </td>
            </tr>
            <tr>
                <td style="background-color: #1f1f1f; padding: 30px; border-radius: 10px;">
                    <h2 style="color: #d2a679; text-align: center;">¡Bienvenido a Eventis, {nombre}!</h2>
                    <p style="font-size: 16px; color: #e0e0e0;">
                        Nos alegra tenerte con nosotros. En Eventis puedes descubrir, crear y asistir a los eventos más interesantes.
                    </p>
                    <p style="font-size: 16px; color: #e0e0e0;">
                        Gracias por confiar en nosotros para gestionar y disfrutar de tus momentos especiales.
                    </p>
                </td>
            </tr>
            <tr>
                <td style="background-color: #2b2b2b; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; color: #aaa;">
                    <p style="margin: 0;">© 2025 Eventis. Todos los derechos reservados.</p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def generar_y_enviar_entrada_qr(usuario_email, usuario_id, evento_id, precio, estado, db,mail,Message):
    try:
        # 1. Insertar entrada en la BBDD
        cur = db.connection.cursor()
        fecha = datetime.now()
        cur.execute("""
            INSERT INTO entradas (usuario_id, evento_id, precio, fecha_compra, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario_id, evento_id, precio, fecha, estado))
        db.connection.commit()

        # Obtener ID de la entrada recién insertada
        entrada_id = cur.lastrowid

        # 2. Crear el contenido del QR
        datos_qr = "Entrada ID: {}\nUsuario ID: {}\nEvento ID: {}".format(entrada_id,usuario_id,evento_id)
        qr_img = qrcode.make(datos_qr)

        # 3. Convertir imagen a bytes
        img_io = BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)

        # 4. Enviar el correo
        msg = Message("Tu entrada para el evento", sender='aaroncm611@gmail.com', recipients=[usuario_email])
        msg.body = "Adjuntamos tu entrada en formato QR puedes presentarla en el evento correspondite. ¡Gracias por tu compra!"
        msg.attach("entrada_qr.png", "image/png", img_io.read())
        mail.send(msg)

        return True

    except Exception as e:
        print("Error al generar/enviar entrada:", e)
        return False
