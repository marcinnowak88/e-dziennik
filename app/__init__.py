from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicjalizacja instancji bazy danych i login managera
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Ustawienie strony logowania
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)

    # Konfiguracja aplikacji
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    login_manager.init_app(app)

    # Importowanie modeli i rejestracja blueprintu w ramach kontekstu aplikacji
    with app.app_context():
        from . import models  # Importuj modele wewnątrz funkcji, aby uniknąć cyklicznego importu
        from .routes import bp as routes_bp  # Importuj blueprint również tutaj
        db.create_all()  # Tworzenie bazy danych, jeśli nie istnieje
        app.register_blueprint(routes_bp)  # Rejestracja blueprintu

    # Funkcja user_loader wymagana przez Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))  # Odwołanie do `models.User` bezpośrednio

    return app

