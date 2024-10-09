from app import db, create_app
from app.models import User, Group
from werkzeug.security import generate_password_hash

def add_and_assign_students():
    app = create_app()
    with app.app_context():
        # Znajdź grupę 1 z "Probabilistyka i statystyka"
        group = Group.query.filter_by(name='Grupa 1').first()

        if not group:
            print("Grupa 1 nie istnieje w bazie danych.")
            return

        # Lista studentów do dodania i przypisania do grupy
        students_data = [
            {'first_name': 'Szymon', 'last_name': 'Andrzejczak'},
            {'first_name': 'Vadym', 'last_name': 'Antoniuk'},
            {'first_name': 'Pavel', 'last_name': 'Ban'},
            {'first_name': 'Grzegorz Paweł', 'last_name': 'Barna'},
            {'first_name': 'Aleksander', 'last_name': 'Baska'},
            {'first_name': 'Łukasz', 'last_name': 'Bączkiewicz'},
            {'first_name': 'Franciszek', 'last_name': 'Broniarczyk'},
            {'first_name': 'Vladyslav', 'last_name': 'Bykovskyi'},
            {'first_name': 'Wiktor', 'last_name': 'Ciesielski'},
            {'first_name': 'Sara Michalina', 'last_name': 'Czabajska'},
            {'first_name': 'Julia Wiktoria', 'last_name': 'Czajkowska'},
            {'first_name': 'Marta Weronika', 'last_name': 'Czujewicz'},
            {'first_name': 'Brunon Aleksander', 'last_name': 'Dłużyński'},
            {'first_name': 'Monika', 'last_name': 'Dubiel'},
            {'first_name': 'Paweł', 'last_name': 'Dur'},
            {'first_name': 'Oleh', 'last_name': 'Dyrda'},
            {'first_name': 'Ihor', 'last_name': 'Semeniuk'},
            {'first_name': 'Bohdan', 'last_name': 'Shvets'},
            {'first_name': 'Łukasz', 'last_name': 'Zieliński'}
        ]

        # Dodaj i przypisz studentów do grupy
        for student_data in students_data:
            # Szukamy studenta po imieniu i nazwisku, nie po username
            existing_student = User.query.filter_by(first_name=student_data['first_name'], last_name=student_data['last_name']).first()

            if not existing_student:
                # Generujemy hash hasła
                hashed_password = generate_password_hash('password123')  # Domyślne hasło dla wszystkich studentów

                # Tworzymy nowego studenta z first_name i last_name
                new_student = User(
                    username=f"{student_data['first_name']}.{student_data['last_name']}",  # Można utworzyć prosty login
                    first_name=student_data['first_name'],  # Wypełniamy pole first_name
                    last_name=student_data['last_name'],    # Wypełniamy pole last_name
                    password=hashed_password,
                    role='student'
                )

                # Dodajemy studenta do sesji
                db.session.add(new_student)
                db.session.commit()  # Komitujemy, aby student miał już ID

                print(f"Dodano studenta: {student_data['first_name']} {student_data['last_name']}")

                # Przypisujemy studenta do grupy
                group.students.append(new_student)
                print(f"Przypisano {student_data['first_name']} {student_data['last_name']} do grupy {group.name}.")
            else:
                print(f"Student {student_data['first_name']} {student_data['last_name']} już istnieje w bazie danych.")

                # Sprawdzamy, czy student już jest w grupie
                if existing_student not in group.students:
                    group.students.append(existing_student)
                    print(f"Przypisano istniejącego studenta {student_data['first_name']} {student_data['last_name']} do grupy {group.name}.")
                else:
                    print(f"Student {student_data['first_name']} {student_data['last_name']} już jest przypisany do grupy {group.name}.")

        # Zatwierdź zmiany w bazie danych na koniec
        db.session.commit()
        print("Wszyscy studenci zostali dodani do bazy danych i przypisani do grupy.")

if __name__ == '__main__':
    add_and_assign_students()
