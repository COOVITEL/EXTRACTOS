from dotenv import load_dotenv
from decrypt import decrypt
import pandas as pd
import cx_Oracle
import os

load_dotenv()

ip = os.getenv('IP')
port = os.getenv('PORT')
#service = decrypt(os.getenv('SERVICENAME'), os.getenv('SERVICEENCRYPT'))
#username = decrypt(os.getenv('USERNAME'), os.getenv('USERNAMEENCRYPT'))
#userpassword = decrypt(os.getenv('PASSWORD'), os.getenv('PASSWORDENCRYPT'))
service = "LINIX"
username = "VISTAS"
userpassword = "VISTAS"


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

        query_users = "SELECT * FROM Ahorr_vist_encab"
        query_movs = "SELECT * FROM Ahorr_vist_movimi"
        cursor.execute(query_movs)

                        # 1037 + CUENTA
        # For you can all dates in the query  use fetchall()
        data = cursor.fetchall()
        #data = cursor.fetchmany(3)
        columns = [desc[0] for desc in cursor.description]
        
        results = [dict(zip(columns, row)) for row in data]

        print(len(results))
        #for result in results:
        #    print(result)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('Error al ejecutar la consulta: %s' % e)
        # Aquí puedes decidir si deseas continuar o terminar el programa
    finally:
        # Asegúrate de cerrar el cursor y la conexión
        cursor.close()
        conn.close()
