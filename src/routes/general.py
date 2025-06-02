from extension.extesion import *

general_bp = Blueprint('general', __name__)

# Funcion para enseñar el inicio(usuario)
@general_bp.route('/', methods=['GET'])
def inicio():
    if request.method == "GET":
        cur = db.connection.cursor()
        cur.execute("SELECT ruta FROM fotos_evento ORDER BY id DESC")
        imagenes = [fila[0] for fila in cur.fetchall()]
        cur.close()
        
        categorias = {
                1: 'Concierto',
                2: 'Teatro',
                3: 'Deporte',
                4: 'Cine',
                5: 'Otros'
        }

        fotos_por_categoria = {}
        for categoria, ruta_foto in ModelUser.obtener_fotos_con_categorias(db):
            fotos_por_categoria[int(categoria)] = ruta_foto
            print(fotos_por_categoria)
        return render_template('inicio.html',imagenes=imagenes, fotos=fotos_por_categoria,categorias=categorias)
    

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
