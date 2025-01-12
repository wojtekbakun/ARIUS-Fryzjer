from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Employee, Service
from backend.extensions import db

# Tworzenie Blueprint dla zarządzania pracownikami
employee_bp = Blueprint("employee", __name__)

# Tworzenie nowego pracownika z usługami
@employee_bp.route("/", methods=["POST"])
@jwt_required()
def create_employee():
    """
    Tworzy nowego pracownika z możliwością przypisania usług.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON

    # Tworzenie nowego obiektu Employee z danymi z żądania
    new_employee = Employee(
        first_name=data.get("first_name"),  # Imię pracownika
        last_name=data.get("last_name"),    # Nazwisko pracownika
        email=data.get("email"),            # Email pracownika
        phone=data.get("phone")             # Numer telefonu pracownika
    )
    
    # Przypisywanie usług (opcjonalnie)
    if "service_ids" in data:
        # Pobranie wszystkich usług, których ID znajdują się w liście 'service_ids'
        services = Service.query.filter(Service.id.in_(data["service_ids"])).all()
        new_employee.services.extend(services)  # Dodanie usług do pracownika

    db.session.add(new_employee)  # Dodanie nowego pracownika do sesji
    db.session.commit()           # Zapisanie zmian w bazie danych
    return jsonify({"message": "Employee created successfully"}), 201  # Zwrócenie odpowiedzi o sukcesie

# Pobieranie listy wszystkich pracowników
@employee_bp.route("/", methods=["GET"])
@jwt_required()
def get_employees():
    """
    Zwraca listę wszystkich pracowników wraz z przypisanymi usługami.
    """
    employees = Employee.query.all()  # Pobranie wszystkich pracowników z bazy danych
    employees_list = []
    for emp in employees:
        # Tworzenie słownika z danymi pracownika
        employees_list.append({
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "email": emp.email,
            "phone": emp.phone,
            "services": [
                {"id": s.id, "name": s.name, "price": s.price} 
                for s in emp.services  # Lista usług przypisanych do pracownika
            ]
        })
    return jsonify(employees_list), 200  # Zwrócenie listy pracowników jako JSON

# Pobieranie danych jednego pracownika
@employee_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    """
    Zwraca dane konkretnego pracownika na podstawie podanego ID.
    """
    employee = Employee.query.get_or_404(employee_id)  # Pobranie pracownika lub zwrócenie 404, jeśli nie istnieje
    employee_data = {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "phone": employee.phone,
        "services": [
            {"id": s.id, "name": s.name, "price": s.price} 
            for s in employee.services  # Lista usług przypisanych do pracownika
        ]
    }
    return jsonify(employee_data), 200  # Zwrócenie danych pracownika jako JSON

# Aktualizacja danych pracownika (w tym przypisanych usług)
@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    """
    Aktualizuje dane istniejącego pracownika, w tym przypisane usługi.
    """
    employee = Employee.query.get_or_404(employee_id)  # Pobranie pracownika lub zwrócenie 404, jeśli nie istnieje
    data = request.get_json()  # Pobranie danych z żądania JSON

    # Aktualizacja podstawowych danych pracownika, jeśli zostały podane
    employee.first_name = data.get("first_name", employee.first_name)  # Aktualizacja imienia
    employee.last_name = data.get("last_name", employee.last_name)      # Aktualizacja nazwiska
    employee.email = data.get("email", employee.email)                  # Aktualizacja emaila
    employee.phone = data.get("phone", employee.phone)                  # Aktualizacja numeru telefonu
    
    # Jeśli chcemy zaktualizować listę usług (np. nadpisać całą listę)
    if "service_ids" in data:
        employee.services.clear()  # Usunięcie obecnych usług przypisanych do pracownika
        # Pobranie nowych usług na podstawie podanych ID
        new_services = Service.query.filter(Service.id.in_(data["service_ids"])).all()
        employee.services.extend(new_services)  # Dodanie nowych usług do pracownika

    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Employee updated successfully"}), 200  # Zwrócenie odpowiedzi o sukcesie

# Usuwanie pracownika
@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id):
    """
    Usuwa istniejącego pracownika na podstawie podanego ID.
    """
    employee = Employee.query.get_or_404(employee_id)  # Pobranie pracownika lub zwrócenie 404, jeśli nie istnieje
    db.session.delete(employee)  # Usunięcie pracownika z sesji
    db.session.commit()           # Zapisanie zmian w bazie danych
    return jsonify({"message": "Employee deleted successfully"}), 200  # Zwrócenie odpowiedzi o sukcesie
