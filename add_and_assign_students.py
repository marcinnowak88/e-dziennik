from app import db, create_app
from app.models import User, Group
from werkzeug.security import generate_password_hash

def add_and_assign_students(group_name, students_data):
    app = create_app()
    with app.app_context():
        # Znajdź grupę po nazwie
        group = Group.query.filter_by(name=group_name).first()

        if not group:
            print(f"{group_name} nie istnieje w bazie danych.")
            return

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
    # Lista studentów do Grupy 2
    students_data_group_2 = [
        {'first_name': 'Marcin', 'last_name': 'Fuks'},
        {'first_name': 'Krzysztof', 'last_name': 'Gębicki'},
        {'first_name': 'Jakub', 'last_name': 'Gibowski'},
        {'first_name': 'Hubert', 'last_name': 'Grabowski'},
        {'first_name': 'Mateusz Łukasz', 'last_name': 'Hałaziński'},
        {'first_name': 'Jakub Wojciech', 'last_name': 'Handke'},
        {'first_name': 'Maksym', 'last_name': 'Havryliak'},
        {'first_name': 'Joannna', 'last_name': 'Heydrych'},
        {'first_name': 'Przemysław Dawid', 'last_name': 'Idczak'},
        {'first_name': 'Ernest', 'last_name': 'Ignyś'},
        {'first_name': 'Igor', 'last_name': 'Jurkowski'},
        {'first_name': 'Daryna', 'last_name': 'Karapysh'},
        {'first_name': 'Violetta', 'last_name': 'Karpchuk'},
        {'first_name': 'Filip', 'last_name': 'Kasprzak'},
        {'first_name': 'Bartosz Wojciech', 'last_name': 'Kiciński'},
        {'first_name': 'Jakub Mikołaj', 'last_name': 'Klimczak'},
        {'first_name': 'Filip Jan', 'last_name': 'Nowicki'},
        {'first_name': 'Franciszek', 'last_name': 'Wojciechowski'}
    ]

    # Wywołujemy funkcję dla Grupy 2
    add_and_assign_students('Grupa 2', students_data_group_2)
