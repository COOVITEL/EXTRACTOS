from dotenv import load_dotenv
import pandas as pd
import cx_Oracle
import os

load_dotenv()

IP = os.getenv('IP')
PORT = os.getenv('PORT')
SERVICE = os.getenv('SERVICENAME')
NAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

def usersBase():
    """ This function calls all users with CA """
    dsn_tns = cx_Oracle.makedsn(IP, PORT, service_name=SERVICE)
    
    try:
        with cx_Oracle.connect(user=NAME, password=PASSWORD, dsn=dsn_tns) as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Ahorr_vist_encab"
                cursor.execute(query)
                #data = cursor.fetchmany(30)
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                users = [dict(zip(columns, row)) for row  in data]
                return users
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 1017:
            print('Error en las credenciales')
        else:
            print(f'Error en la conexión en la base de datos: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')


if __name__ == '__main__':
    usersBase()