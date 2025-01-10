from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Payment
from backend.extensions import db
from backend.models import User

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/payment", methods=["POST"])
@jwt_required()
def create_payment():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_payment = Payment(user_id=user_id, amount=data["amount"], status="pending")
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment created"}), 201


@payment_bp.route("/invoice-data", methods=["GET"])
@jwt_required()
def invoice_data():
    auth_user_email = get_jwt_identity()
    user = User.query.filter_by(email=auth_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    invoice_data = {
        "id": user.id,
        "email": user.email,
        "street": user.street,
        "street_number": user.street_number,
        "postal_code": user.postal_code,
        "city": user.city,
        "nip": user.nip,
        "company_name": user.company_name,
        "purchase_date": user.created_at.strftime("%Y-%m-%d")
    }

    return jsonify(invoice_data)

@payment_bp.route("/invoice-data", methods=["POST"])
@jwt_required()
def update_invoice_data():
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