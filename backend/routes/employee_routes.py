from flask import Blueprint, jsonify, request
from backend.models import Employee
from backend.extensions import db
from flask_jwt_extended import jwt_required

employee_bp = Blueprint("employee", __name__)

# Tworzenie nowego pracownika
@employee_bp.route("/employee", methods=["POST"])
@jwt_required()
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone=data.get("phone"),
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee created successfully"}), 201

# Pobieranie listy wszystkich pracowników
@employee_bp.route("/", methods=["GET"])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    employees_list = [
        {
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "email": emp.email,
            "phone": emp.phone,
        }
        for emp in employees
    ]
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
    }
    return jsonify(employee_data), 200

# Aktualizacja danych pracownika
@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required()
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    employee.first_name = data.get("first_name", employee.first_name)
    employee.last_name = data.get("last_name", employee.last_name)
    employee.email = data.get("email", employee.email)
    employee.phone = data.get("phone", employee.phone)
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