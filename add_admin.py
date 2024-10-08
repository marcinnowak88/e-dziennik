from werkzeug.security import generate_password_hash
from app import db
from app.models import User
from run import app

def create_admin():
    with app.app_context():
        # Sprawdź, czy użytkownik admin już istnieje
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin is None:
            # Utwórz nowego administratora z zahashowanym hasłem
            admin_user = User(username='admin', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print('Administrator został pomyślnie dodany.')
        else:
            print('Administrator już istnieje, aktualizuję hasło.')
            # Zaktualizuj hasło, aby było poprawnie zahashowane
            existing_admin.password = generate_password_hash('admin123')
            db.session.commit()
            print('Hasło administratora zostało zaktualizowane.')

if __name__ == '__main__':
    create_admin()
