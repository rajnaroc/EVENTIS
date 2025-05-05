from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,EmailField,PasswordField,DateField
from wtforms.validators import DataRequired,Length,Email,EqualTo

# forms para el login 
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

# forms para el registro de un nuevo usuario
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
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
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

# forms para editar el perfil de un usuario
class perfilform(FlaskForm):
    nombre = StringField("Escribe tu nombre", validators=[
        DataRequired(),
        Length(min=4)
    ])
    correo = EmailField("Escribe tu correo", validators=[
        DataRequired(),
        Length(max=25),
        Email()
    ])
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
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
