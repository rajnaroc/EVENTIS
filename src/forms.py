from flask_wtf import FlaskForm
import re
from datetime import date
from wtforms import SubmitField,StringField,EmailField,PasswordField,DateField,TextAreaField,FloatField,IntegerField,SelectField,MultipleFileField
from wtforms.validators import DataRequired,Length,Email,EqualTo,NumberRange,InputRequired,ValidationError

# Funcion para poner una contraseña segura
# Función para verificar complejidad de la contraseña
def password_complexity_check(form, field):
    password = field.data
    pattern = re.compile(
        r'^(?=.*[a-z])'            # al menos una minúscula
        r'(?=.*[A-Z])'             # al menos una mayúscula
        r'(?=.*\d)'                # al menos un número
        r'(?=.*[@$!%*?&])'         # al menos un carácter especial
        r'[A-Za-z\d@$!%*?&]{6,12}$'  # solo caracteres permitidos y longitud
    )
    if not pattern.match(password):
        raise ValidationError("La contraseña debe tener entre 6 y 12 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales (@$!%*?&).")

#Funcion limitar el uso de la cuentas a 16 años o 80 años maximo
def edad_valida(form, field):
    hoy = date.today()
    edad = hoy.year - field.data.year - ((hoy.month, hoy.day) < (field.data.month, field.data.day))

    if edad < 16 or edad > 80:
        raise ValidationError("Debes tener entre 16 y 80 años.")

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
        DataRequired(),
        edad_valida
        ])
    contraseña = PasswordField("Escribe tu Contraseña", validators=[
        DataRequired(),
        Length(min=6,max=12),
        password_complexity_check,
        EqualTo("confirme",message="La contraseña debe ser igual al de abajo")
    ])
    confirme = PasswordField("Repite tu Contraseña", validators=[
        DataRequired(),
        Length(min=6, max=12),
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
        DataRequired(),
        edad_valida
        ])
    enviar = SubmitField("Cambiar Datos")

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
    password = PasswordField('Nueva contraseña', validators=[
        DataRequired(), 
        Length(min=6),
        password_complexity_check
    ])
    submit = SubmitField('Cambiar contraseña')