from backend.extensions import db
from datetime import datetime

# Tabela asocjacyjna dla relacji wiele-do-wielu (Employee <-> Service)
employee_services = db.Table(
    "employee_services",
    db.Column("employee_id", db.Integer, db.ForeignKey("employee.id"), primary_key=True),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(150), nullable=True)       # Ulica
    street_number = db.Column(db.String(20), nullable=True) # Numer ulicy
    postal_code = db.Column(db.String(20), nullable=True)   # Kod pocztowy
    city = db.Column(db.String(100), nullable=True)         # Miejscowość
    nip = db.Column(db.String(20), nullable=True)           # NIP
    company_name = db.Column(db.String(200), nullable=True) # Nazwa firmy/instytucji

class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)

    # Relacja wiele-do-wielu z Employee
    employees = db.relationship(
        "Employee",
        secondary="employee_services",  # nazwa tabeli asocjacyjnej
        back_populates="services"
    )

class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="scheduled")  # scheduled, completed, canceled

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)  
    last_name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    phone = db.Column(db.String(20), nullable=True)

    # Relacja wiele-do-wielu z Service
    services = db.relationship(
        "Service",
        secondary="employee_services",  # nazwa tabeli asocjacyjnej
        back_populates="employees"
    )