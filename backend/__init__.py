from flask import Flask
from backend.extensions import db, migrate, jwt, cors
from backend.routes import register_blueprints  
from backend.config import Config


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