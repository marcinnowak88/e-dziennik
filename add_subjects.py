# add_subjects.py

from app import db, create_app
from app.models import Subject

def add_subjects():
    app = create_app()
    with app.app_context():
        # Lista przedmiotów do dodania
        subjects = [
            Subject(name='Matematyka dyskretna'),
            Subject(name='Probabilistyka i statystyka'),
            Subject(name='Podstawy zarządzania')
        ]

        # Dodaj przedmioty do sesji
        db.session.add_all(subjects)

        # Zatwierdź zmiany w bazie danych
        db.session.commit()

        print('Przedmioty zostały pomyślnie dodane.')

if __name__ == '__main__':
    add_subjects()
