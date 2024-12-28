from flask import Flask
from backend.extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object("backend.config.Config")

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Zarejestruj blueprinty
    from backend.routes import main_bp
    app.register_blueprint(main_bp)

    return app