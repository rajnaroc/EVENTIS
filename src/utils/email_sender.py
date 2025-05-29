import os
import qrcode
from io import BytesIO
from datetime import datetime
from io import BytesIO
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

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

def generar_y_enviar_entrada_qr(usuario_email, usuario_id, evento_id, precio, estado, db, mail, Message):
    try:
        cur = db.connection.cursor()

        # Obtener nombre del usuario
        cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cur.fetchone()
        if not resultado:
            raise Exception("Usuario no encontrado.")
        nombre_usuario = resultado[0]

        # Insertar entrada
        fecha = datetime.now()
        cur.execute("""
            INSERT INTO entradas (usuario_id, evento_id, precio, fecha_compra, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (usuario_id, evento_id, precio, fecha, estado))
        db.connection.commit()
        entrada_id = cur.lastrowid

        # Generar QR
        datos_qr = f"Entrada ID: {entrada_id}\nUsuario ID: {usuario_id}\nEvento ID: {evento_id}"
        qr_img = qrcode.make(datos_qr)

        # Crear PDF con datos + QR
        pdf_io = BytesIO()
        c = canvas.Canvas(pdf_io, pagesize=A4)
        c.setFont("Helvetica", 12)

        c.drawString(2 * cm, 27 * cm, f"Nombre: {nombre_usuario}")
        c.drawString(2 * cm, 26 * cm, f"Correo: {usuario_email}")
        c.drawString(2 * cm, 25 * cm, f"ID Entrada: {entrada_id}")

        # Insertar imagen QR correctamente
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_image = ImageReader(qr_buffer)
        c.drawImage(qr_image, 2 * cm, 15 * cm, width=8 * cm, height=8 * cm)


        c.showPage()
        c.save()
        pdf_io.seek(0)

        # 5. Enviar correo con HTML y PDF adjunto
        msg = Message("Tu entrada para el evento", sender='aaroncm611@gmail.com', recipients=[usuario_email])
        msg.html = """
        <h2>Hola {},</h2>
        <p>Gracias por tu compra. Adjuntamos tu entrada en formato PDF, que incluye un código QR único.</p>
        <p>Por favor, preséntala en el acceso al evento.</p>
        <p>Saludos,<br><strong>Eventis</strong></p>
        """.format(nombre_usuario)
        msg.attach("entrada_evento.pdf", "application/pdf", pdf_io.read())
        mail.send(msg)

        return True

    except Exception as e:
        print("Error al generar/enviar entrada:", e)
        return False