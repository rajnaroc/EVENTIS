from datetime import datetime, date, timedelta


# filtro para poner el tiempo bien

def format_hora(td):
    if hasattr(td, 'total_seconds'):
        total_seconds = int(td.total_seconds())
    else:
        # Si es string tipo "HH:MM:SS", parsear a timedelta
        try:
            h, m, s = map(int, td.split(':'))
            td = timedelta(hours=h, minutes=m, seconds=s)
            total_seconds = int(td.total_seconds())
        except Exception:
            return td  # Devuelve el string tal cual si no puede parsear

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"


# filtro para poder enseñar la fecha bien
def format_fecha(value):
    # Si es string, pasamos a date
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%d-%m-%Y').date()
        except ValueError:
            return value  # Si no puede parsear, devuelve tal cual

    if isinstance(value, date):
        return value.strftime('%d/%m/%Y')
    
    # Si no es ni str ni date, devuelve el valor tal cual
    return value