from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User
from backend.extensions import db

# Tworzenie Blueprint dla uwierzytelniania
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Rejestruje nowego użytkownika.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON

    # Walidacja wymaganych pól
    if not data.get("email") or not data.get("password"):
        # Zwrócenie błędu, jeśli brak emaila lub hasła
        return jsonify({"error": "Email and password are required"}), 400

    # Generowanie zaszyfrowanego hasła
    hashed_password = generate_password_hash(data["password"])

    # Tworzenie nowego użytkownika z dodatkowymi danymi
    new_user = User(
        email=data["email"],
        password=hashed_password,
        first_name=data.get("first_name"),          # Opcjonalne pole: Imię
        last_name=data.get("last_name"),            # Opcjonalne pole: Nazwisko
        street=data.get("street"),                  # Opcjonalne pole: Ulica
        street_number=data.get("street_number"),    # Opcjonalne pole: Numer ulicy
        postal_code=data.get("postal_code"),        # Opcjonalne pole: Kod pocztowy
        city=data.get("city"),                      # Opcjonalne pole: Miejscowość
        nip=data.get("nip"),                        # Opcjonalne pole: NIP
        company_name=data.get("company_name")       # Opcjonalne pole: Nazwa firmy/instytucji
    )

    db.session.add(new_user)  # Dodanie nowego użytkownika do sesji
    db.session.commit()       # Zapisanie zmian w bazie danych
    return jsonify({"message": "User registered successfully"}), 201  # Zwrócenie sukcesu

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Loguje użytkownika i zwraca token dostępu.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON
    user = User.query.filter_by(email=data["email"]).first()  # Wyszukanie użytkownika po emailu

    # Sprawdzenie, czy użytkownik istnieje i czy hasło jest poprawne
    if user and check_password_hash(user.password, data["password"]):
        # Generowanie tokenu dostępu
        access_token = create_access_token(identity=user.email)
        return jsonify({"token": access_token, "email": user.email}), 200  # Zwrócenie tokenu i emaila

    # Zwrócenie błędu, jeśli dane logowania są nieprawidłowe
    return jsonify({"message": "Invalid credentials"}), 401
