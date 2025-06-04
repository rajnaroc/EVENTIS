from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,EmailField,PasswordField,DateField,TextAreaField,FloatField,IntegerField,SelectField,MultipleFileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,NumberRange,InputRequired

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

# forms para crear eventos y editarlos
class crearEventoForm(FlaskForm):
    titulo = StringField('Título', validators=[
        DataRequired(), Length(max=200)
        ])
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired()
        ])
    fecha = DateField('Fecha del evento',format='%Y-%m-%d', validators=[
        DataRequired()
        ])
    hora_inicio = StringField('Hora Inicio', validators=[
        DataRequired(), Length(max=5)
        
        ])
    hora_fin = StringField('Hora Fin', validators=[
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
        InputRequired(message="El precio es obligatorio"),  # acepta 0 como válido
        NumberRange(min=0, message="El precio no puede ser negativo")
        ])
    aforo = IntegerField('Aforo máximo', validators=[
        DataRequired(), NumberRange(min=1)
        ])
    fotos = MultipleFileField('Fotos', validators=[
        Length(max=5, message="Se permiten un máximo de 10 fotos")
        ])
    submit = SubmitField('Crear evento')
    submit_editar = SubmitField('Editar evento')

class CambiarContraseñaForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Cambiar contraseña')