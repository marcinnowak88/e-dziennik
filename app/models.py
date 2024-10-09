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
    username = db.Column(db.String(150), unique=True, nullable=False)  # Używane przez adminów i nauczycieli
    first_name = db.Column(db.String(150), nullable=True)  # Tylko dla studentów
    last_name = db.Column(db.String(150), nullable=True)  # Tylko dla studentów
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'teacher', 'student'
    grade = db.Column(db.Float, nullable=True)  # Nowa kolumna na ocenę

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
