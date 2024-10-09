# add_groups.py

from app import db, create_app
from app.models import Subject, Group

def add_groups():
    app = create_app()
    with app.app_context():
        # Znajdź przedmioty w bazie danych
        matematyka_dyskretna = Subject.query.filter_by(name='Matematyka dyskretna').first()
        probabilistyka_i_statystyka = Subject.query.filter_by(name='Probabilistyka i statystyka').first()

        if not matematyka_dyskretna:
            print('Przedmiot "Matematyka dyskretna" nie istnieje w bazie danych.')
            return

        if not probabilistyka_i_statystyka:
            print('Przedmiot "Probabilistyka i statystyka" nie istnieje w bazie danych.')
            return

        # Dodaj grupy do "Matematyka dyskretna"
        grupy_matematyka = [
            Group(name='Grupa 5', subject_id=matematyka_dyskretna.id),
            Group(name='Grupa 6', subject_id=matematyka_dyskretna.id)
        ]

        # Dodaj grupy do "Probabilistyka i statystyka"
        grupy_probabilistyka = [
            Group(name='Grupa 1', subject_id=probabilistyka_i_statystyka.id),
            Group(name='Grupa 2', subject_id=probabilistyka_i_statystyka.id),
            Group(name='Grupa 3', subject_id=probabilistyka_i_statystyka.id),
            Group(name='Grupa 4', subject_id=probabilistyka_i_statystyka.id)
        ]

        # Dodaj wszystkie grupy do sesji
        db.session.add_all(grupy_matematyka + grupy_probabilistyka)

        # Zatwierdź zmiany w bazie danych
        db.session.commit()

        print('Grupy zostały pomyślnie dodane.')

if __name__ == '__main__':
    add_groups()
