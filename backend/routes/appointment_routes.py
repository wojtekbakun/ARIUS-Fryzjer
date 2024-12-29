from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Service, Appointment
from backend.extensions import db

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([{"id": s.id, "name": s.name, "price": s.price} for s in services])

@appointment_bp.route("/appointments", methods=["POST"])
@jwt_required()
def create_appointment():
    data = request.get_json()
    user_id = get_jwt_identity()["id"]
    new_appointment = Appointment(user_id=user_id, service_id=data["service_id"], date=data["date"])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created"}), 201

@appointment_bp.route("/appointments", methods=["GET"])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()["id"]
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": a.id,
        "service": a.service_id,
        "date": a.date,
        "status": a.status
    } for a in appointments])