from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Service, Appointment, Employee
from backend.extensions import db
from datetime import datetime

# Tworzenie Blueprint dla zarządzania wizytami
appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/", methods=["POST"])
@jwt_required()
def create_appointment():
    """
    Tworzy nową wizytę z możliwością przypisania pracownika.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika

    # Walidacja danych wejściowych
    try:
        appointment_date_str = data["date"]  # Pobranie daty wizyty jako string
        appointment_date_obj = datetime.strptime(appointment_date_str, "%Y-%m-%d %H:%M:%S")  # Konwersja stringa na obiekt datetime
    except (KeyError, ValueError):
        # Zwrócenie błędu, jeśli data jest nieprawidłowa lub brakująca
        return jsonify({"error": "Invalid or missing 'date' format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    employee_id = data.get("employee_id")  # Pobranie opcjonalnego ID pracownika
    if employee_id and not Employee.query.get(employee_id):
        # Zwrócenie błędu, jeśli podany pracownik nie istnieje
        return jsonify({"error": "Employee with given ID not found."}), 404

    # Tworzenie nowego obiektu Appointment
    new_appointment = Appointment(
        user_id=user_id,
        service_id=data["service_id"],
        employee_id=employee_id,
        date=appointment_date_obj,
        status=data.get("status", "scheduled")  # Ustawienie statusu, domyślnie "scheduled"
    )
    db.session.add(new_appointment)  # Dodanie wizyty do sesji
    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Appointment created"}), 201  # Zwrócenie sukcesu

@appointment_bp.route("/", methods=["GET"])
@jwt_required()
def get_appointments():
    """
    Zwraca wszystkie wizyty zalogowanego użytkownika.
    """
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika
    appointments = Appointment.query.filter_by(user_id=user_id).all()  # Pobranie wszystkich wizyt użytkownika
    
    # Przygotowanie listy wizyt do zwrócenia jako JSON
    return jsonify([
        {
            "id": a.id,
            "service_id": a.service_id,
            "employee_id": a.employee_id,
            "date": a.date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        }
        for a in appointments
    ])

@appointment_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_appointments():
    """
    Zwraca wszystkie wizyty (terminy) wszystkich użytkowników.
    """
    appointments = Appointment.query.all()  # Pobranie wszystkich wizyt z bazy danych
    
    # Przygotowanie listy wszystkich wizyt do zwrócenia jako JSON
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "service_id": a.service_id,
            "employee_id": a.employee_id,
            "date": a.date.strftime("%Y-%m-%d %H:%M:%S"),
            "status": a.status
        }
        for a in appointments
    ]), 200  # Zwrócenie sukcesu

# Edycja wizyty
@appointment_bp.route("/<int:appointment_id>", methods=["PUT"])
@jwt_required()
def update_appointment(appointment_id):
    """
    Edytuje istniejącą wizytę (zmiana usługi, daty, statusu lub pracownika).
    """
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika
    # Wyszukanie wizyty o podanym ID i przypisanej do użytkownika
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=user_id).first()
    
    if not appointment:
        # Zwrócenie błędu, jeśli wizyta nie została znaleziona
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()  # Pobranie danych z żądania JSON
    if "service_id" in data:
        appointment.service_id = data["service_id"]  # Aktualizacja ID usługi
    if "employee_id" in data:
        employee_id = data["employee_id"]
        if not Employee.query.get(employee_id):
            # Zwrócenie błędu, jeśli podany pracownik nie istnieje
            return jsonify({"error": "Employee with given ID not found."}), 404
        appointment.employee_id = employee_id  # Aktualizacja ID pracownika
    if "date" in data:
        try:
            appointment_date_obj = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")  # Konwersja stringa na datetime
            appointment.date = appointment_date_obj  # Aktualizacja daty wizyty
        except ValueError:
            # Zwrócenie błędu, jeśli format daty jest nieprawidłowy
            return jsonify({"error": "Invalid 'date' format. Use 'YYYY-MM-DD HH:MM:SS'."}), 400
    if "status" in data:
        appointment.status = data["status"]  # Aktualizacja statusu wizyty
    
    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Appointment updated successfully"}), 200  # Zwrócenie sukcesu

# Usuwanie wizyty
@appointment_bp.route("/<int:appointment_id>", methods=["DELETE"])
@jwt_required()
def delete_appointment(appointment_id):
    """
    Usuwa istniejącą wizytę.
    """
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika
    # Wyszukanie wizyty o podanym ID i przypisanej do użytkownika
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=user_id).first()
    
    if not appointment:
        # Zwrócenie błędu, jeśli wizyta nie została znaleziona
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appointment)  # Usunięcie wizyty z sesji
    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Appointment deleted successfully"}), 200  # Zwrócenie sukcesu
