from flask import Flask, jsonify
from backend.extensions import db, migrate, jwt, cors
from backend.routes import register_blueprints  
from backend.config import Config


@jwt.invalid_token_loader
def invalid_token_callback(err):
    return jsonify({"msg": "Invalid token"}), 422

@jwt.expired_token_loader
def expired_token_callback(err, token):
    return jsonify({"msg": "Token has expired"}), 401

@jwt.unauthorized_loader
def missing_token_callback(err):
    return jsonify({"msg": "Missing token"}), 401

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    register_blueprints(app)

    


    return app