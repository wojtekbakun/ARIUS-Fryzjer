import os

class Config:
    SECRET_KEY = "supersecretkey"  # Klucz dla ogólnej ochrony Flask
    JWT_SECRET_KEY = "another_super_secret_key"  # Klucz używany przez JWT
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False