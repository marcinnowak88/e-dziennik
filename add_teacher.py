from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User  # Zmieniony import, aby wskazywał na katalog 'app'

# Ścieżka do istniejącej bazy danych SQLite w katalogu 'instance'
DATABASE_PATH = 'sqlite:///instance/app.db'

# Utworzenie połączenia z bazą danych
engine = create_engine(DATABASE_PATH)
Session = sessionmaker(bind=engine)
session = Session()

# Funkcja do dodania nauczyciela
def create_teacher():
    # Sprawdzenie, czy nauczyciel już istnieje
    existing_teacher = session.query(User).filter_by(username='marcinnowak').first()

    if existing_teacher is None:
        # Tworzenie nowego nauczyciela
        new_teacher = User(
            username='marcinnowak',
            password=generate_password_hash('12345'),  # Haszowanie hasła
            role='teacher'
        )

        # Dodanie nauczyciela do bazy danych
        session.add(new_teacher)
        session.commit()
        print('Nauczyciel został pomyślnie dodany.')
    else:
        print('Nauczyciel o podanym loginie już istnieje.')

# Uruchomienie funkcji
if __name__ == '__main__':
    create_teacher()
    # Zamknięcie sesji
    session.close()
