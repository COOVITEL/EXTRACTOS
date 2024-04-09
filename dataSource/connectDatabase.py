import cx_Oracle

ip = '192.168.1.12'
port = '1521'
service = 'LINIX'
username = 'VISTAS'
userpassword = 'VISTAS'

# Configuración de la conexión
dsn_tns = cx_Oracle.makedsn(ip, port, service_name=service)

try:
    conn = cx_Oracle.connect(user=username, password=userpassword, dsn=dsn_tns)
except cx_Oracle.DatabaseError as e:
    error, = e.args
    if error.code == 1017:
        print('Por favor, verifica tus credenciales.')
    else:
        print('Error de conexión a la base de datos: %s' % e)
    # Aquí puedes decidir si deseas continuar o terminar el programa
    # sys.exit()

# Ejemplo de consulta
if conn:
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM <TU_TABLA>')
        for row in cursor:
            print(row)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('Error al ejecutar la consulta: %s' % e)
        # Aquí puedes decidir si deseas continuar o terminar el programa
    finally:
        # Asegúrate de cerrar el cursor y la conexión
        cursor.close()
        conn.close()
