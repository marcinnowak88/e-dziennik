from app import create_app, db
from app.models import User, Subject, Group  # Dodano import modeli

app = create_app()

with app.app_context():
    db.create_all()  # Tworzy wszystkie tabele w bazie danych na podstawie modeli
    print("Tabele zostały utworzone w bazie danych.")
