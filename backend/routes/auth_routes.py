from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User
from backend.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Walidacja wymaganych pól
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    hashed_password = generate_password_hash(data["password"])

    # Tworzenie nowego użytkownika z dodatkowymi danymi
    new_user = User(
        email=data["email"],
        password=hashed_password,
        street=data.get("street"),
        street_number=data.get("street_number"),
        postal_code=data.get("postal_code"),
        city=data.get("city"),
        nip=data.get("nip"),
        company_name=data.get("company_name")
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.email)
        return jsonify({"token": access_token, "email": user.email}), 200
    return jsonify({"message": "Invalid credentials"}), 401