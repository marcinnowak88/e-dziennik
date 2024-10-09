from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User, Subject  # Dodaj Subject, jeśli potrzebny w admin_dashboard
from .forms import LoginForm
from . import db

# Utwórz blueprint
bp = Blueprint('main', __name__)

# Trasa logowania
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Znajdź użytkownika w bazie danych
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Witaj, {user.username}!', 'success')

            # Przekieruj do odpowiedniego dashboardu na podstawie roli
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('main.teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('main.student_dashboard'))
            else:
                # Jeśli rola nie jest rozpoznana, przekieruj do logowania lub wyloguj
                flash('Nieznana rola użytkownika.', 'danger')
                return redirect(url_for('main.logout'))
        else:
            flash('Nieprawidłowy login lub hasło', 'danger')

    return render_template('login.html', form=form)

# Trasa wylogowania
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany!', 'success')
    return redirect(url_for('main.login'))

# Strona główna
@bp.route('/')
def index():
    if current_user.is_authenticated:
        # Przekieruj do odpowiedniego dashboardu
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('main.teacher_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('main.student_dashboard'))
        else:
            flash('Nieznana rola użytkownika.', 'danger')
            return redirect(url_for('main.logout'))
    else:
        return redirect(url_for('main.login'))

# Dashboard dla administratora
@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Nie masz uprawnień dostępu do tej strony.', 'danger')
        return redirect(url_for('main.login'))
    # Pobierz dane potrzebne do wyświetlenia na stronie administratora
    teachers = User.query.filter_by(role='teacher').all()
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', user=current_user, teachers=teachers, subjects=subjects)

# Dashboard dla nauczyciela
@bp.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        flash('Nie masz uprawnień dostępu do tej strony.', 'danger')
        return redirect(url_for('main.login'))
    # Pobierz dane potrzebne do wyświetlenia na stronie nauczyciela
    # np. listę przedmiotów, grup, etc.
    return render_template('teacher_dashboard.html', user=current_user)

# Dashboard dla studenta
@bp.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Nie masz uprawnień dostępu do tej strony.', 'danger')
        return redirect(url_for('main.login'))
    # Pobierz dane potrzebne do wyświetlenia na stronie studenta
    # np. oceny, harmonogram, etc.
    return render_template('student_dashboard.html', user=current_user)


@bp.route('/dashboard')
@login_required
def dashboard():
    # Przekieruj do odpowiedniego dashboardu na podstawie roli
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('main.teacher_dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('main.student_dashboard'))
    else:
        flash('Nieznana rola użytkownika.', 'danger')
        return redirect(url_for('main.logout'))
