from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User
from extensions import db

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    auth_user_email = get_jwt_identity()
    user = User.query.filter_by(email=auth_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Dane do faktury
    user_data = {
        "email": user.email,
        "id": user.id,
        "street": user.street,
        "street_number": user.street_number,
        "postal_code": user.postal_code,
        "city": user.city,
        "nip": user.nip,
        "company_name": user.company_name,
        "purchase_date": user.created_at.strftime("%Y-%m-%d")  # Data zakupu usługi
    }
    
    return jsonify(user_data)

@user_bp.route("/profile", methods=["POST"])
@jwt_required()
def update_user_data():
    auth_user_email = get_jwt_identity()
    user = User.query.filter_by(email=auth_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.street = data.get("street", user.street)
    user.street_number = data.get("street_number", user.street_number)
    user.postal_code = data.get("postal_code", user.postal_code)
    user.city = data.get("city", user.city)
    user.nip = data.get("nip", user.nip)
    user.company_name = data.get("company_name", user.company_name)

    db.session.commit()
    return jsonify({"message": "Invoice data updated successfully"})