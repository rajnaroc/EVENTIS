import os

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
