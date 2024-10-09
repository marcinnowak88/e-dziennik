from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Znajdź użytkownika o loginie 'nauczyciel1'
    user = User.query.filter_by(username='nauczyciel1').first()

    if user:
        # Zaktualizuj dane użytkownika
        user.first_name = 'Marcin'
        user.last_name = 'Nowak'

        # Zatwierdź zmiany w bazie danych
        db.session.commit()

        print(f"Zmieniono dane użytkownika na: {user.first_name} {user.last_name} (login: {user.username}).")
    else:
        print("Użytkownik 'nauczyciel1' nie został znaleziony.")
