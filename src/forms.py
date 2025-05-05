from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,EmailField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class loginform(FlaskForm):
    correo = EmailField("Escribe tu correo", validators=[
        DataRequired(),
        Length(max=25),
        Email()
    ])
    contraseña = PasswordField("Escribe tu Contraseña", validators=[
        DataRequired(),
        Length(min=6,max=12)
    ])
    enviar = SubmitField("Iniciar sesion")

class registerForm(FlaskForm):
    nombre = StringField("Escribe tu nombre", validators=[
        DataRequired(),
        Length(min=4)
    ])
    correo = EmailField("Escribe tu correo", validators=[
        DataRequired(),
        Length(max=25),
        Email()
    ])
    contraseña = PasswordField("Escribe tu Contraseña", validators=[
        DataRequired(),
        Length(min=6,max=12),
        EqualTo("confirme",message="Repite la contrasela")
    ])
    confirme = PasswordField("Repite tu Contraseña", validators=[
        DataRequired(),
        Length(min=6, max=12)
    ])
    enviar = SubmitField("Register")
