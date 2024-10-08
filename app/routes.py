from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User, Subject
from .forms import LoginForm, UserForm  # Zakładamy, że dodasz formularz UserForm do obsługi użytkowników
from . import db

# Utwórz blueprint
bp = Blueprint('main', __name__)

# Panel administratora - lista nauczycieli i przedmiotów
@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Sprawdź, czy zalogowany użytkownik jest administratorem
    if current_user.role != 'admin':
        flash('Nie masz dostępu do tej strony.', 'danger')
        return redirect(url_for('main.index'))  # Użyj poprawnej nazwy blueprintu

    # Pobierz listę nauczycieli i przedmiotów z bazy danych
    teachers = User.query.filter_by(role='teacher').all()
    subjects = Subject.query.all()

    return render_template('admin_dashboard.html', teachers=teachers, subjects=subjects)



# Trasa do dodawania użytkowników (jeśli wymagana)
@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))

    # Pobierz wszystkich użytkowników z bazy danych
    users = User.query.all()

    # Obsługa dodawania nowego użytkownika
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('main.admin'))

    return render_template('admin.html', users=users, form=form)

# Trasa logowania
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(f"Znaleziono użytkownika: {user.username}, rola: {user.role}")
        else:
            print("Nie znaleziono użytkownika o podanej nazwie.")

        if user and check_password_hash(user.password, form.password.data):  # Użyj check_password_hash
            login_user(user)
            print(f"Zalogowano użytkownika: {user.username}")

            # Sprawdź rolę użytkownika i przekieruj na odpowiednią stronę
            if user.role == 'admin':
                print("Przekierowywanie na /admin/dashboard")
                return redirect(url_for('main.admin_dashboard'))
            else:
                print("Przekierowywanie na /dashboard")
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
            print("Nieprawidłowa nazwa użytkownika lub hasło")

    return render_template('login.html', form=form)

# Trasa do wylogowania
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Trasa do panelu użytkownika
@bp.route('/dashboard')
@login_required
def dashboard():
    # Kod wyświetlający panel dla zalogowanego użytkownika
    return render_template('dashboard.html', user=current_user)

# Trasa do strony głównej
@bp.route('/')
def index():
    return render_template('index.html')


from werkzeug.security import generate_password_hash
from run import app

# Tymczasowy kod do dodania lub aktualizacji administratora
def create_admin():
    with app.app_context():
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin is None:
            admin_user = User(username='admin', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print('Administrator został pomyślnie dodany.')
        else:
            print('Administrator już istnieje, aktualizuję hasło.')
            existing_admin.password = generate_password_hash('admin123')
            db.session.commit()
            print('Hasło administratora zostało zaktualizowane.')

# Wywołanie funkcji, aby dodać lub zaktualizować administratora
create_admin()