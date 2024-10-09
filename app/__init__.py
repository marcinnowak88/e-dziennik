from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Utwórz instancję SQLAlchemy i LoginManager
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Nowa ścieżka do bazy danych w katalogu 'app'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Dodano tę linię

    # Inicjalizacja SQLAlchemy i LoginManager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Dodaj tę linię

    # Zarejestrowanie blueprintów
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Import modeli (musi być po zainicjalizowaniu bazy danych)
    from .models import User, Subject, Group

    return app



# Funkcja ładowania użytkownika
@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import User w funkcji
    return User.query.get(int(user_id))
