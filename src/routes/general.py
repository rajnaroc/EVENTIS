from extension.extesion import *

general_bp = Blueprint('general', __name__)

# Funcion para enseñar el inicio(usuario)
@general_bp.route('/', methods=['GET'])
def inicio():
    cursor = db.connection.cursor()
    cursor.execute("SELECT ruta FROM fotos_evento ORDER BY id DESC")
    imagenes = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    return render_template('inicio.html',imagenes=imagenes)

# Ruta para mostrar la Política de Privacidad(usuario)
@general_bp.route('/politicas')
def politica_privacidad():
    return render_template('politica_privacidad.html')

# Ruta para mostrar Terminos y Condiciones(usuario)
@general_bp.route('/terminoscondiciones')
def terminos_condiciones():
    return render_template('terminos_condiciones.html')

# Ruta para mostrar el Aviso Legal(usuario)
@general_bp.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso_legal.html')
