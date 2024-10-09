# add_users.py
from werkzeug.security import generate_password_hash
from app import db, create_app
from app.models import User

def create_users():
    app = create_app()
    with app.app_context():
        # Dodaj nauczyciela
        teacher = User(username='nauczyciel2', password=generate_password_hash('nauczyciel123'), role='teacher')
        db.session.add(teacher)

        # Dodaj studenta
        student = User(username='student2', password=generate_password_hash('student123'), role='student')
        db.session.add(student)

        db.session.commit()
        print('Użytkownicy zostali pomyślnie dodani.')

if __name__ == '__main__':
    create_users()
