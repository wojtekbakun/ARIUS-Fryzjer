from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Employee, Service
from backend.extensions import db

employee_bp = Blueprint("employee", __name__)

# Tworzenie nowego pracownika z usługami
@employee_bp.route("/", methods=["POST"])
@jwt_required()
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone=data.get("phone")
    )
    
    # Przypisywanie usług (opcjonalnie)
    if "service_ids" in data:
        services = Service.query.filter(Service.id.in_(data["service_ids"])).all()
        new_employee.services.extend(services)

    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee created successfully"}), 201

# Pobieranie listy wszystkich pracowników
@employee_bp.route("/", methods=["GET"])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    employees_list = []
    for emp in employees:
        employees_list.append({
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "email": emp.email,
            "phone": emp.phone,
            "services": [
                {"id": s.id, "name": s.name, "price": s.price} 
                for s in emp.services
            ]
        })
    return jsonify(employees_list), 200

# Pobieranie danych jednego pracownika
@employee_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee_data = {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "phone": employee.phone,
        "services": [
            {"id": s.id, "name": s.name, "price": s.price} 
            for s in employee.services
        ]
    }
    return jsonify(employee_data), 200

# Aktualizacja danych pracownika (w tym przypisanych usług)
@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()

    employee.first_name = data.get("first_name", employee.first_name)
    employee.last_name = data.get("last_name", employee.last_name)
    employee.email = data.get("email", employee.email)
    employee.phone = data.get("phone", employee.phone)
    
    # Jeśli chcemy zaktualizować listę usług (np. nadpisać całą listę)
    if "service_ids" in data:
        employee.services.clear()  # czyścimy obecną listę usług
        new_services = Service.query.filter(Service.id.in_(data["service_ids"])).all()
        employee.services.extend(new_services)

    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200

# Usuwanie pracownika
@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200