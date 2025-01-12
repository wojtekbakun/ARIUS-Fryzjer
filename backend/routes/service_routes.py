from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import Service
from backend.extensions import db

# Tworzenie Blueprint dla zarządzania usługami
service_bp = Blueprint("service", __name__)

# Tworzenie nowej usługi
@service_bp.route("/", methods=["POST"])
@jwt_required()
def create_service():
    """
    Tworzy nową usługę.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON
    
    # Tworzenie nowego obiektu Service z danymi z żądania
    new_service = Service(
        name=data.get("name"),              # Nazwa usługi
        description=data.get("description"),# Opis usługi
        price=data.get("price")             # Cena usługi
    )
    db.session.add(new_service)  # Dodanie nowej usługi do sesji
    db.session.commit()           # Zapisanie zmian w bazie danych
    
    # Zwrócenie odpowiedzi z komunikatem o sukcesie i statusem 201 (Created)
    return jsonify({"message": "Service created successfully"}), 201

# Pobieranie listy wszystkich usług
@service_bp.route("/", methods=["GET"])
@jwt_required()
def get_services():
    """
    Zwraca listę wszystkich usług.
    """
    services = Service.query.all()  # Pobranie wszystkich usług z bazy danych
    services_list = []
    
    for service in services:
        # Dodanie szczegółów każdej usługi do listy
        services_list.append({
            "id": service.id,                  # Unikalny identyfikator usługi
            "name": service.name,              # Nazwa usługi
            "description": service.description,# Opis usługi
            "price": service.price             # Cena usługi
        })
        
    # Zwrócenie listy usług jako odpowiedź JSON z kodem statusu 200 (OK)
    return jsonify(services_list), 200

# Pobieranie szczegółów pojedynczej usługi
@service_bp.route("/<int:service_id>", methods=["GET"])
@jwt_required()
def get_service(service_id):
    """
    Zwraca szczegóły konkretnej usługi na podstawie podanego ID.
    """
    service = Service.query.get_or_404(service_id)  # Pobranie usługi lub zwrócenie 404, jeśli nie istnieje
    return jsonify({
        "id": service.id,                  # Unikalny identyfikator usługi
        "name": service.name,              # Nazwa usługi
        "description": service.description,# Opis usługi
        "price": service.price             # Cena usługi
    }), 200  # Zwrócenie danych usługi jako JSON z kodem statusu 200 (OK)

# Aktualizacja usługi
@service_bp.route("/<int:service_id>", methods=["PUT"])
@jwt_required()
def update_service(service_id):
    """
    Aktualizuje istniejącą usługę.
    """
    service = Service.query.get_or_404(service_id)  # Pobranie usługi lub zwrócenie 404, jeśli nie istnieje
    data = request.get_json()  # Pobranie danych z żądania JSON
    
    # Aktualizacja danych usługi na podstawie danych z żądania
    service.name = data.get("name", service.name)               # Aktualizacja nazwy, jeśli podano
    service.description = data.get("description", service.description) # Aktualizacja opisu, jeśli podano
    service.price = data.get("price", service.price)            # Aktualizacja ceny, jeśli podano
    
    db.session.commit()  # Zapisanie zmian w bazie danych
    return jsonify({"message": "Service updated successfully"}), 200  # Zwrócenie komunikatu o sukcesie

# Usuwanie usługi
@service_bp.route("/<int:service_id>", methods=["DELETE"])
@jwt_required()
def delete_service(service_id):
    """
    Usuwa istniejącą usługę na podstawie podanego ID.
    """
    service = Service.query.get_or_404(service_id)  # Pobranie usługi lub zwrócenie 404, jeśli nie istnieje
    db.session.delete(service)  # Usunięcie usługi z sesji
    db.session.commit()          # Zapisanie zmian w bazie danych
    return jsonify({"message": "Service deleted successfully"}), 200  # Zwrócenie komunikatu o sukcesie
