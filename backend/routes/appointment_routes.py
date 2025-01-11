from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Service, Appointment
from backend.extensions import db
from datetime import datetime

appointment_bp = Blueprint("appointment", __name__)


@appointment_bp.route("/", methods=["POST"])
@jwt_required()
def create_appointment():
    data = request.get_json()
    user_id = get_jwt_identity()
    appointment_date_str = data["date"]
    appointment_date_obj = datetime.strptime(appointment_date_str, "%Y-%m-%d %H:%M:%S")
    
    new_appointment = Appointment(
        user_id=user_id,
        service_id=data["service_id"],
        date=appointment_date_obj
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created"}), 201

@appointment_bp.route("/", methods=["GET"])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    
    return jsonify([
        {
            "id": a.id,
            "service": a.service_id,
            "date": a.date.strftime("%Y-%m-%d %H:%M:%S"),  # formatowanie daty
            "status": a.status
        } 
        for a in appointments
    ])

# Edycja wizyty
@appointment_bp.route("/<int:appointment_id>", methods=["PUT"])
@jwt_required()
def update_appointment(appointment_id):
    user_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=user_id).first()
    
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()
    if "service_id" in data:
        appointment.service_id = data["service_id"]
    if "date" in data:
        appointment_date_obj = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
        appointment.date = appointment_date_obj
    if "status" in data:
        appointment.status = data["status"]
    
    db.session.commit()
    return jsonify({"message": "Appointment updated successfully"}), 200

# Usuwanie wizyty
@appointment_bp.route("/<int:appointment_id>", methods=["DELETE"])
@jwt_required()
def delete_appointment(appointment_id):
    user_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=user_id).first()
    
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"}), 200