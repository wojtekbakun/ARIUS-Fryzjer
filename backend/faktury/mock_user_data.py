import random
from faker import Faker
from backend.extensions import db
from backend.models import User, Service, Payment, Appointment

fake = Faker()

def create_mock_users(n=10):
    users = []
    for _ in range(n):
        user = User(
            email=fake.email(),
            password=fake.password(length=12),
            role="user",
            street=fake.street_name(),
            street_number=str(fake.building_number()),
            postal_code=fake.postcode(),
            city=fake.city(),
            nip=fake.numerify(text='###-###-##-##'),
            company_name=fake.company()
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users

def create_mock_services(n=5):
    services = []
    for _ in range(n):
        service = Service(
            name=fake.word().capitalize() + " Service",
            description=fake.sentence(),
            price=round(random.uniform(100, 1000), 2)
        )
        db.session.add(service)
        services.append(service)
    db.session.commit()
    return services

def create_mock_payments(users, n=10):
    payments = []
    for _ in range(n):
        user = random.choice(users)
        payment = Payment(
            user_id=user.id,
            amount=round(random.uniform(150, 1500), 2),
            status=random.choice(["pending", "completed", "failed"])
        )
        db.session.add(payment)
        payments.append(payment)
    db.session.commit()
    return payments

def create_mock_appointments(users, services, n=10):
    for _ in range(n):
        user = random.choice(users)
        service = random.choice(services)
        appointment = Appointment(
            user_id=user.id,
            service_id=service.id,
            date=fake.date_time_between(start_date="-1y", end_date="now"),
            status=random.choice(["scheduled", "completed", "canceled"])
        )
        db.session.add(appointment)
    db.session.commit()

def generate_all_mock_data():
    users = create_mock_users(20)
    services = create_mock_services(10)
    create_mock_payments(users, 30)
    create_mock_appointments(users, services, 30)

if __name__ == "__main__":
    with db.session.begin():
        generate_all_mock_data()
    print("Mock data has been generated successfully.")
