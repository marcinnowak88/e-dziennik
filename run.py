from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Sprawdzenie, czy użytkownik admin już istnieje
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Jeśli nie istnieje, stwórz użytkownika admina
        new_admin = User(username='admin', password='admin123', role='admin')
        db.session.add(new_admin)
        db.session.commit()
        print("Administrator account created: username='admin', password='admin123'")
    else:
        print("Administrator account already exists.")

if __name__ == '__main__':
    app.run(debug=True)
