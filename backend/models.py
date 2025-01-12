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

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator użytkownika
    email = db.Column(db.String(120), unique=True, nullable=False)  # Adres e-mail użytkownika
    password = db.Column(db.String(200), nullable=False)  # Hasło użytkownika (zaszyfrowane)
    role = db.Column(db.String(50), default="user")  # Rola użytkownika, np. 'user', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data i czas utworzenia konta
    first_name = db.Column(db.String(100), nullable=True)  # Imię użytkownika
    last_name = db.Column(db.String(100), nullable=True)  # Nazwisko użytkownika
    street = db.Column(db.String(150), nullable=True)       # Ulica adresu użytkownika
    street_number = db.Column(db.String(20), nullable=True) # Numer ulicy
    postal_code = db.Column(db.String(20), nullable=True)   # Kod pocztowy
    city = db.Column(db.String(100), nullable=True)         # Miejscowość
    nip = db.Column(db.String(20), nullable=True)           # Numer identyfikacji podatkowej (NIP)
    company_name = db.Column(db.String(200), nullable=True) # Nazwa firmy lub instytucji użytkownika

class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator usługi
    name = db.Column(db.String(100), nullable=False)  # Nazwa usługi
    description = db.Column(db.String(255))  # Opis usługi
    price = db.Column(db.Float, nullable=False)  # Cena usługi

    # Relacja wiele-do-wielu z Employee
    employees = db.relationship(
        "Employee",
        secondary="employee_services",  # Nazwa tabeli asocjacyjnej
        back_populates="services"  # Powiązanie z atrybutem 'services' w modelu Employee
    )

class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator wizyty
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID użytkownika, który zarezerwował wizytę
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)  # ID usługi związanej z wizytą
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=True)  # ID przypisanego pracownika
    date = db.Column(db.DateTime, nullable=False)  # Data i czas wizyty
    status = db.Column(db.String(50), default="scheduled")  # Status wizyty, np. 'scheduled', 'completed', 'canceled'

    # Relacje z innymi modelami
    user = db.relationship("User", backref="appointments")  # Relacja do modelu User
    service = db.relationship("Service", backref="appointments")  # Relacja do modelu Service
    employee = db.relationship("Employee", backref="appointments")  # Relacja do modelu Employee

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator recenzji
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID użytkownika, który dodał recenzję
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)  # ID usługi, której dotyczy recenzja
    rating = db.Column(db.Integer, nullable=False)  # Ocena usługi (np. od 1 do 5)
    comment = db.Column(db.Text)  # Komentarz do recenzji

class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator płatności
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # ID użytkownika dokonującego płatności
    amount = db.Column(db.Float, nullable=False)  # Kwota płatności
    status = db.Column(db.String(50), default="pending")  # Status płatności, np. 'pending', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data i czas utworzenia płatności

    # Dodatkowe pola dla faktury
    invoice_name = db.Column(db.String(200), nullable=True)  # Nazwa faktury
    invoice_sent = db.Column(db.Boolean, default=False)      # Czy faktura została wysłana
    services_details = db.Column(db.Text, nullable=True)     # Szczegóły usług (JSON w formie tekstu)
    total_cost = db.Column(db.Float, nullable=True)          # Całkowity koszt usług
    invoice_date = db.Column(db.DateTime, nullable=True)     # Data wystawienia faktury

class Employee(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)  # Unikalny identyfikator pracownika
    first_name = db.Column(db.String(100), nullable=False)  # Imię pracownika
    last_name = db.Column(db.String(100), nullable=False)  # Nazwisko pracownika
    email = db.Column(db.String(120), unique=True, nullable=False)  # Adres e-mail pracownika
    phone = db.Column(db.String(20), nullable=True)  # Numer telefonu pracownika

    # Relacja wiele-do-wielu z Service
    services = db.relationship(
        "Service",
        secondary="employee_services",  # Nazwa tabeli asocjacyjnej
        back_populates="employees"  # Powiązanie z atrybutem 'employees' w modelu Service
    )
