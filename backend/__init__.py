from flask import Flask, jsonify
from backend.extensions import db, migrate, jwt, cors
from backend.routes import register_blueprints  
from backend.config import Config
import logging

# Obsługa błędów JWT
@jwt.invalid_token_loader
def invalid_token_callback(err):
    logging.error("Invalid token error: %s", err)  # Dodano logowanie błędu
    return jsonify({"msg": "Invalid token"}), 422

@jwt.expired_token_loader
def expired_token_callback(err, token):
    logging.warning("Token has expired: %s", token)  # Dodano logowanie ostrzeżenia
    return jsonify({"msg": "Token has expired"}), 401

@jwt.unauthorized_loader
def missing_token_callback(err):
    logging.error("Missing token error: %s", err)  # Dodano logowanie błędu
    return jsonify({"msg": "Missing token"}), 401

def create_app():
    # Konfiguracja loggera
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicjalizacja rozszerzeń
    logging.debug("Initializing extensions...")
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    logging.debug("Extensions initialized.")

    # Rejestracja tras
    logging.debug("Registering blueprints...")
    register_blueprints(app)
    logging.debug("Blueprints registered.")

    # Obsługa błędów HTTP
    @app.errorhandler(404)
    def not_found_error(error):
        logging.error("Resource not found: %s", error)
        return jsonify({"msg": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.critical("Internal server error: %s", error)
        return jsonify({"msg": "Internal server error"}), 500

    # Testowy endpoint do debugowania
    @app.route("/health", methods=["GET"])
    def health_check():
        logging.info("Health check endpoint called.")
        return jsonify({"status": "OK"}), 200

    # Dodanie trybu debugowania na podstawie konfiguracji
    if app.config.get("DEBUG", False):
        logging.info("Application running in debug mode.")

    logging.info("Application initialized successfully.")
    return app