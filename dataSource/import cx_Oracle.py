import cx_Oracle

username = 'VISTAS'
password = 'VISTAS'
hostname = '192.168.1.12'
port = '1521'
database = 'LINIX'

try:
    connect = cx_Oracle.makedsn(hostname, port, database)
    print(connect)
    
    connection = cx_Oracle.connect(username, password, connect, encoding="UTF-8")
    print(connection)
    
    cursor = connection.cursor()
    cursor.execute('SELECT table_name FROM user_tables')

except Exception as e:
    print(e)