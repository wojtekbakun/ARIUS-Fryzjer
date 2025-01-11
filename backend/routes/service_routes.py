from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import Service
from backend.extensions import db

service_bp = Blueprint("service", __name__)

# Tworzenie nowej usługi
@service_bp.route("/", methods=["POST"])
@jwt_required()
def create_service():
    data = request.get_json()
    
    new_service = Service(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price")
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully"}), 201

# Pobieranie listy wszystkich usług
@service_bp.route("/", methods=["GET"])
@jwt_required()
def get_services():
    services = Service.query.all()
    services_list = []
    
    for service in services:
        services_list.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price
        })
        
    return jsonify(services_list), 200

# Pobieranie szczegółów pojedynczej usługi
@service_bp.route("/<int:service_id>", methods=["GET"])
@jwt_required()
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify({
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "price": service.price
    }), 200

# Aktualizacja usługi
@service_bp.route("/<int:service_id>", methods=["PUT"])
@jwt_required()
def update_service(service_id):
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    
    service.name = data.get("name", service.name)
    service.description = data.get("description", service.description)
    service.price = data.get("price", service.price)
    
    db.session.commit()
    return jsonify({"message": "Service updated successfully"}), 200

# Usuwanie usługi
@service_bp.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200