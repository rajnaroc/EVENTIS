
def correo_exite(correo,db):
    try:
        cur = db.connection.cursor()
            
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        data = cur.fetchone()
        if data:
            return True
        return False
    except Exception as e:
        print(e)
        return False

