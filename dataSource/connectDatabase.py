import cx_Oracle
import pandas as pd
from decrypt import decrypt

ip = '192.168.1.139'
port = '1521'
service = decrypt('krfojra', 'valkiria')
username = decrypt('nqcpb', 'ciphernewman')
userpassword = decrypt('gqtmk', 'vigenerepython')


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
        query = """
                    SELECT K_CUENTA K_CUENTA_AH136
                        ,A_NUMCTA
                        ,N_NUMCTA
                        ,K_CLASIF
                        ,I_ESTADO
                        ,K_IDTERC_ASO
                        ,pk_ah_saldo.fu_v_saldo_actual_dia
                                            (k_cuenta,
                                            '21050501',
                                            k_sucurs,
                                            :P_F_CORTE_HAS
                                            ) SALDOFIN
                        FROM AH136MCUENTA
                        where i_estado = 'A'
                """
        cursor.execute("""
                       SELECT CEDULA, NNASOCIA, REGIONAL, CUENTA, ESTADO FROM BI_AHORRO_VISTA_MES WHERE ESTADO IS NOT NULL
                       """)
                        # 1037 + CUENTA
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        results = [dict(zip(columns, row)) for row in data]

        
        print(len(results))

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print('Error al ejecutar la consulta: %s' % e)
        # Aquí puedes decidir si deseas continuar o terminar el programa
    finally:
        # Asegúrate de cerrar el cursor y la conexión
        cursor.close()
        conn.close()
