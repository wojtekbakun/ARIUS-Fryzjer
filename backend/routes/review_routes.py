from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Review
from backend.extensions import db

# Tworzenie Blueprint dla zarządzania opiniami
review_bp = Blueprint("review", __name__)

@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():
    """
    Tworzy nową opinię użytkownika.
    """
    data = request.get_json()  # Pobranie danych z żądania JSON
    user_id = get_jwt_identity()  # Pobranie ID zalogowanego użytkownika za pomocą JWT

    # Tworzenie nowego obiektu Review z danymi z żądania
    new_review = Review(
        user_id=user_id,  # ID użytkownika dodającego opinię
        service_id=data["service_id"],  # ID usługi, której dotyczy opinia
        rating=data["rating"],  # Ocena usługi
        comment=data["comment"]  # Komentarz do opinii
    )
    db.session.add(new_review)  # Dodanie nowej opinii do sesji
    db.session.commit()  # Zapisanie zmian w bazie danych

    # Zwrócenie odpowiedzi z komunikatem o sukcesie i statusem 201 (Created)
    return jsonify({"message": "Review submitted"}), 201

@review_bp.route("/", methods=["GET"])
def get_reviews():
    """
    Zwraca listę wszystkich opinii w bazie danych.
    """
    reviews = Review.query.all()  # Pobranie wszystkich opinii z bazy danych
    reviews_list = []
    for r in reviews:
        # Dodanie szczegółów każdej opinii do listy
        reviews_list.append({
            "id": r.id,  # Unikalny identyfikator opinii
            "user_id": r.user_id,  # ID użytkownika, który dodał opinię
            "service_id": r.service_id,  # ID usługi, której dotyczy opinia
            "rating": r.rating,  # Ocena usługi
            "comment": r.comment  # Komentarz do opinii
        })

    # Zwrócenie listy opinii jako odpowiedź JSON z kodem statusu 200 (OK)
    return jsonify(reviews_list), 200
