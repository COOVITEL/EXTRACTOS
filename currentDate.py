monthsYear = {
    "01": 'Enero',
    "02": 'Febrero',
    "03": 'Marzo',
    "04": 'Abril',
    "05": 'Mayo',
    "06": 'Junio',
    "07": 'Julio',
    "08": 'Agosto',
    "09": 'Septiembre',
    "10": 'Octubre',
    "11": 'Noviembre',
    "12": 'Diciembre'
}

def current(init, end):
    """"""
    dates = init.split("-")
    print(dates)
    start = dates[1]
    last = end.split("-")[2]
    month = monthsYear[dates[1]]
    return f"{start} de {month} al {last} {dates[0]}"
    