from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import User
from .forms import LoginForm, UserForm  # Zakładamy, że dodasz formularz UserForm do obsługi użytkowników
from . import db
# Utwórz blueprint
bp = Blueprint('main', __name__)

# Panel administratora - lista użytkowników
@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
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
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin_dashboard.html', users=users, form=form)

# Trasa logowania
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Pamiętaj o hashowaniu haseł w rzeczywistych aplikacjach!
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
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
    # Przykład użycia current_user do pobrania informacji o zalogowanym użytkowniku
    return render_template('dashboard.html', user=current_user)

# Trasa do strony głównej (lub innej)
@bp.route('/')
def index():
    return render_template('index.html')


