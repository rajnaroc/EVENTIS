from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,EmailField,PasswordField,DateField,TextAreaField,DecimalField,IntegerField,SelectField,DateTimeLocalField
from wtforms.validators import DataRequired,Length,Email,EqualTo,NumberRange
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
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[
        DataRequired()
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
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[
        DataRequired()
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

# forms para el contacto
class contactoform(FlaskForm):
    nombre = StringField("Escribe tu nombre", validators=[
        DataRequired(),
        Length(min=4)
    ])
    correo = EmailField("Escribe tu correo", validators=[
        DataRequired(),
        Length(max=25),
        Email()
    ])
    mensaje = TextAreaField("Motivo del asunto", validators=[
        DataRequired(),
        Length(min=4)
    ])
    enviar = SubmitField("Enviar")

class crearEventoForm(FlaskForm):
    titulo = StringField('Título', validators=[
        DataRequired(), Length(max=200)
        ])
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired()
        ])
    fecha = DateTimeLocalField('Fecha y hora', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired()
        ])
    lugar = StringField('Lugar', validators=[
        DataRequired(), Length(max=200)
        ])
    imagen = StringField('URL de la imagen', validators=[
        DataRequired(), Length(max=255)
        ])
    categoria = SelectField('Categoría', coerce=int, validators=[
        DataRequired()
        ])
    precio = DecimalField('Precio (€)', validators=[
        DataRequired(), NumberRange(min=0)
        ])
    aforo = IntegerField('Aforo máximo', validators=[
        DataRequired(), NumberRange(min=1)
        ])
    submit = SubmitField('Crear evento')