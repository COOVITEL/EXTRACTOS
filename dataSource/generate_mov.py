from faker import Faker
import random

fake = Faker()

def generate_mov():
    return {
        "fecha": f"{random.randint(1, 30)}-FEB-24",
        "lugar": fake.city(),
        "documento": fake.random_number(digits=9),
        "sucursal": fake.random_number(digits=3),
        "debito": random.randint(500000, 5000000),
        "credito": random.randint(500000, 5000000),
        "saldos": random.randint(1000000, 10000000)
    }