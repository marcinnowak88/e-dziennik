from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inicjalizacja bazy danych i menedżera logowania
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
        try:
            from . import models  # Importuj modele
            print("Import modeli zakończony.")
            db.create_all()  # Tworzenie tabel w bazie danych
            print("Tabele zostały utworzone.")

            # Sprawdź, czy użytkownik już istnieje
            #if not models.User.query.filter_by(username="test_user").first():
            #   test_user = models.User(username="test_user", password="test_password", role="admin")
            #   db.session.add(test_user)
            #  db.session.commit()
            #  print("Testowy użytkownik został dodany.")
            #else:
              #  print("Użytkownik 'test_user' już istnieje.")
        except Exception as e:
            print(f"Błąd podczas inicjalizacji bazy danych: {e}")

    # Rejestracja blueprintu
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)  # Rejestracja blueprintu

    # Funkcja user_loader wymagana przez Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))  # Odwołanie do `models.User` bezpośrednio

    return app
