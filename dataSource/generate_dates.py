from faker import Faker
import random
import json
from generate_mov import generate_mov

fake = Faker()

def main():

    datos_users = []
    for _ in range(5):
        usuario = {
            "username": fake.user_name(),
            "cedula": fake.random_number(digits=8),
            "city": fake.city(),
            "cuenta": fake.random_number(digits=10),
            "estado": "Activo",
            "saldo_anterior": random.randint(1000, 5000),
            "saldo_actual": random.randint(1000, 5000),
            "debitos": random.randint(500000, 10000000),
            "creditos": random.randint(500000, 5000000),
            "movimientos": [generate_mov() for _ in range(random.randint(15, 35))]
        }
        datos_users.append(usuario)
    
    datos_json = json.dumps(datos_users, indent=4)
    
    with open('data.py', 'w') as archive:
        archive.write(datos_json)

if __name__ == '__main__':
    main()



