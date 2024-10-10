from . import db
from flask_login import UserMixin

# Tabela asocjacyjna dla relacji wiele do wielu między użytkownikami (studentami) a grupami
group_student = db.Table('group_student',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

# Model użytkownika
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=True)  # Tylko dla studentów
    last_name = db.Column(db.String(150), nullable=True)  # Tylko dla studentów
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'teacher', 'student'

    # Relacja z grupami (dla studentów)
    groups = db.relationship('Group', secondary='group_student', back_populates='students')

# Model przedmiotu
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relacja z grupami
    groups = db.relationship('Group', back_populates='subject', lazy=True)

# Model grupy
class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

    # Relacja z przedmiotem
    subject = db.relationship('Subject', back_populates='groups')

    # Relacja z użytkownikami (studentami)
    students = db.relationship('User', secondary=group_student, back_populates='groups')

# Model ocen dla każdego studenta
class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Identyfikator studenta
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)  # Identyfikator grupy
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)  # Identyfikator przedmiotu
    kolokwium1 = db.Column(db.Float, nullable=True)
    kolokwium2 = db.Column(db.Float, nullable=True)
    projekt = db.Column(db.Float, nullable=True)
    aktywnosc = db.Column(db.Float, nullable=True)
    inne = db.Column(db.Float, nullable=True)
    uwagi = db.Column(db.Text, nullable=True)
    grade = db.Column(db.Float, nullable=True)  # Ocena końcowa

    # Relacje
    student = db.relationship('User')
    group = db.relationship('Group')
    subject = db.relationship('Subject')
