from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User
from backend.extensions import db

# Tworzenie Blueprint dla zarządzania użytkownikami
user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """
    Zwraca profil zalogowanego użytkownika.
    """
    auth_user_email = get_jwt_identity()  # Pobranie emaila zalogowanego użytkownika z tokenu JWT
    user = User.query.filter_by(email=auth_user_email).first()  # Wyszukanie użytkownika w bazie danych na podstawie emaila
    
    if not user:
        # Zwrócenie błędu, jeśli użytkownik nie zostanie znaleziony
        return jsonify({"error": "User not found"}), 404
    
    # Przygotowanie danych użytkownika do zwrócenia
    user_data = {
        "id": user.id,                      # Unikalny identyfikator użytkownika
        "email": user.email,                # Email użytkownika
        "first_name": user.first_name,      # Imię użytkownika
        "last_name": user.last_name,        # Nazwisko użytkownika
        "street": user.street,              # Ulica adresu użytkownika
        "street_number": user.street_number,# Numer ulicy
        "postal_code": user.postal_code,    # Kod pocztowy
        "city": user.city,                  # Miejscowość
        "nip": user.nip,                    # Numer identyfikacji podatkowej (NIP)
        "company_name": user.company_name,  # Nazwa firmy lub instytucji użytkownika
    }
    
    # Zwrócenie danych użytkownika jako odpowiedź JSON
    return jsonify(user_data), 200

@user_bp.route("/profile", methods=["POST"])
@jwt_required()
def update_user_data():
    """
    Aktualizuje dane profilu zalogowanego użytkownika.
    """
    auth_user_email = get_jwt_identity()  # Pobranie emaila zalogowanego użytkownika z tokenu JWT
    user = User.query.filter_by(email=auth_user_email).first()  # Wyszukanie użytkownika w bazie danych na podstawie emaila
    
    if not user:
        # Zwrócenie błędu, jeśli użytkownik nie zostanie znaleziony
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()  # Pobranie danych z żądania JSON

    # Aktualizacja danych użytkownika na podstawie danych z żądania
    user.first_name = data.get("first_name", user.first_name)            # Aktualizacja imienia, jeśli podano
    user.last_name = data.get("last_name", user.last_name)                # Aktualizacja nazwiska, jeśli podano
    user.street = data.get("street", user.street)                        # Aktualizacja ulicy, jeśli podano
    user.street_number = data.get("street_number", user.street_number)    # Aktualizacja numeru ulicy, jeśli podano
    user.postal_code = data.get("postal_code", user.postal_code)          # Aktualizacja kodu pocztowego, jeśli podano
    user.city = data.get("city", user.city)                              # Aktualizacja miejscowości, jeśli podano
    user.nip = data.get("nip", user.nip)                                # Aktualizacja NIP, jeśli podano
    user.company_name = data.get("company_name", user.company_name)      # Aktualizacja nazwy firmy/instytucji, jeśli podano

    db.session.commit()  # Zapisanie zmian w bazie danych

    # Zwrócenie odpowiedzi z komunikatem o sukcesie
    return jsonify({"message": "Profile data updated successfully"}), 200
