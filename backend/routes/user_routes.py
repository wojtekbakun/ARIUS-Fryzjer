from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    auth_user_email = get_jwt_identity()
    user =  User.query.filter_by(email=auth_user_email).first()
    return jsonify({"email": auth_user_email, "id": user.id})