from datetime import datetime, date


# filtro para poner el tiempo bien
def format_hora(td):
    total_seconds = int(td.total_seconds())
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