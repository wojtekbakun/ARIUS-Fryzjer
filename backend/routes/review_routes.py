from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Review
from backend.extensions import db

review_bp = Blueprint("review", __name__)

@review_bp.route("/reviews", methods=["POST"])
@jwt_required()
def create_review():
    data = request.get_json()
    user_id = get_jwt_identity()["id"]
    new_review = Review(user_id=user_id, service_id=data["service_id"], rating=data["rating"], comment=data["comment"])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "Review submitted"}), 201