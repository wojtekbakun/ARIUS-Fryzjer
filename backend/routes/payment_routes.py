from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Payment
from backend.extensions import db

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