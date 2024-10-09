from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Znajdujemy wszystkich studentów, którzy mają None w polach first_name lub last_name
    students_with_none = User.query.filter(
        (User.first_name == None) | (User.last_name == None),  # Sprawdza, czy first_name lub last_name jest None
        User.role == 'student'
    ).all()

    # Usuwamy tych studentów z bazy
    for student in students_with_none:
        print(f"Usuwanie studenta z None w danych: {student.username}")
        db.session.delete(student)

    # Zatwierdzamy zmiany
    db.session.commit()

    print("Studenci z None w danych zostali usunięci.")
