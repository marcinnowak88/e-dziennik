from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User, Subject, Group, Assessment
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

    # Pobierz wszystkie przedmioty z bazy danych
    subjects = Subject.query.all()

    return render_template('teacher_dashboard.html', user=current_user, subjects=subjects)

# Dashboard dla studenta
@bp.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Nie masz uprawnień dostępu do tej strony.', 'danger')
        return redirect(url_for('main.login'))

    return render_template('student_dashboard.html', user=current_user)

# Trasa dla ogólnego dashboardu
@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('main.teacher_dashboard'))
    elif current_user.role == 'student':
        return redirect(url_for('main.student_dashboard'))
    else:
        flash('Nieznana rola użytkownika.', 'danger')
        return redirect(url_for('main.logout'))

# Trasa wyświetlająca listę studentów przypisanych do grupy
@bp.route('/group/<int:group_id>/students', methods=['GET', 'POST'])
@login_required
def group_students(group_id):
    # Znajdź grupę
    group = Group.query.get_or_404(group_id)
    subject = group.subject  # Znajdź przedmiot powiązany z grupą

    # Znajdź wszystkich studentów przypisanych do tej grupy
    students = group.students

    if request.method == 'POST':
        for student in students:
            # Znajdź lub utwórz nowy rekord w Assessment
            assessment = Assessment.query.filter_by(student_id=student.id, group_id=group.id,
                                                    subject_id=subject.id).first()
            if not assessment:
                assessment = Assessment(student_id=student.id, group_id=group.id, subject_id=subject.id)

            # Pobierz dane z formularza, jeśli puste to ustaw na None
            kolokwium1 = request.form.get(f'kolokwium1_{student.id}')
            kolokwium2 = request.form.get(f'kolokwium2_{student.id}')
            projekt = request.form.get(f'projekt_{student.id}')
            aktywnosc = request.form.get(f'aktywnosc_{student.id}')
            inne = request.form.get(f'inne_{student.id}')
            uwagi = request.form.get(f'uwagi_{student.id}')
            grade = request.form.get(f'grade_{student.id}')

            # Przypisz wartości lub None, jeśli puste
            assessment.kolokwium1 = float(kolokwium1) if kolokwium1 else None
            assessment.kolokwium2 = float(kolokwium2) if kolokwium2 else None
            assessment.projekt = float(projekt) if projekt else None
            assessment.aktywnosc = float(aktywnosc) if aktywnosc else None
            assessment.inne = float(inne) if inne else None
            assessment.uwagi = uwagi if uwagi else None
            assessment.grade = float(grade) if grade else None

            # Dodaj/aktualizuj w bazie danych
            db.session.add(assessment)

        # Zatwierdź zmiany w bazie
        db.session.commit()
        flash('Dane zostały zapisane!', 'success')
        return redirect(url_for('main.group_students', group_id=group.id))

    # Pobierz istniejące oceny dla tej grupy i przedmiotu
    assessments = {a.student_id: a for a in Assessment.query.filter_by(group_id=group.id, subject_id=subject.id).all()}

    return render_template('group_students.html', group=group, students=students, assessments=assessments)
