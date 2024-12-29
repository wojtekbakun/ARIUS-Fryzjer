from flask import Blueprint

# Importowanie blueprintów z podmodułów
from .auth_routes import auth_bp
from .user_routes import user_bp
from .appointment_routes import appointment_bp
from .review_routes import review_bp
from .payment_routes import payment_bp

# Opcjonalne: agregowanie wszystkich blueprintów w jednym miejscu (do automatycznej rejestracji)
all_blueprints = [
    (auth_bp, "/auth"),
    (user_bp, "/user"),
    (appointment_bp, "/appointments"),
    (review_bp, "/reviews"),
    (payment_bp, "/payments"),
]

def register_blueprints(app):
    """
    Funkcja rejestrująca wszystkie blueprinty w aplikacji Flask.
    """
    for blueprint, url_prefix in all_blueprints:
        print(f"Rejestruję blueprint: {blueprint.name} z prefiksem: {url_prefix}")
        app.register_blueprint(blueprint, url_prefix=url_prefix)