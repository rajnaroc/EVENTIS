from re import S
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,EmailField,PasswordField,DateField,TextAreaField,FloatField,IntegerField,SelectField,DateTimeField,MultipleFileField
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
        Length(max=50),
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
    fecha = DateField('Fecha del evento',format='%d-%m-%Y', validators=[
        DataRequired(
            
        )])
    hora = StringField('Hora', validators=[
        DataRequired(), Length(max=5)
        ])
    lugar = StringField('Lugar', validators=[
        DataRequired(), Length(max=200)
        ])
    categoria = SelectField('Categoría', choices=[
        (0, 'Selecciona una categoría'),
            (1, 'Concierto'),
            (2, 'Teatro'),
            (3, 'Deporte'),
            (4, 'Cine'),
            (5, 'Otros')
        ])
    precio = FloatField('Precio (€)', validators=[
        DataRequired(), NumberRange(min=0)
        ])
    aforo = IntegerField('Aforo máximo', validators=[
        DataRequired(), NumberRange(min=1)
        ])
    fotos = MultipleFileField('Fotos', validators=[
        DataRequired(),
        Length(max=5, message="Se permiten un máximo de 5 fotos")
        ])
    submit = SubmitField('Crear evento')
    submit_fotos = SubmitField('Subir fotos')