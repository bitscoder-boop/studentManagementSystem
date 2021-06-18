from .import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    grade_number = db.Column(db.String(12), unique=True, nullable = False)
    students = db.relationship('Student', backref='grade')
    total_subject = db.Column(db.Integer)
    classteachers = db.relationship('Staff', backref = 'class_teacher', uselist = False)
    subjects = db.relationship('Subject', backref='grade')

    def assign_classTeacher(self, teacherName):
        teacher = Staff.query.filter_by(username = teacherName).first()
        self.classteachers = teacher

    def __repr__(self):
        return f'<Class: {self.grade_number}>'


ACCESS = {
        'student': 0,
        'staff':1
        }

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(24), index = True)
    middle_name = db.Column(db.String(24), nullable = True)
    last_name = db.Column(db.String(24))
    username = db.Column(db.String(24), unique = True)
    gender = db.Column(db.String(12))
    address = db.Column(db.Text(length = 100))
    seson_start_year = db.Column(db.DateTime, default = datetime.utcnow)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default= ACCESS['student'])
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable= False, default = '0000')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Student {self.username}>'


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(24), index = True)
    middle_name = db.Column(db.String(24), nullable = True)
    last_name = db.Column(db.String(24))
    username = db.Column(db.String(24), unique = True)
    gender = db.Column(db.String(12))
    address = db.Column(db.Text(length = 100))
    email = db.Column(db.String(24), unique = True)
    contact = db.Column(db.Integer, unique = True)
    seson_start_year = db.Column(db.DateTime, default = datetime.utcnow)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable = True)
    role = db.Column(db.Integer, default= ACCESS['staff'])
    password_hash = db.Column(db.String(128))
    grade_subject = db.relationship('Subject', backref='teacher', uselist = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def assign_classTeaching(self, gradeToTeach):
        value = Grade.query.filter_by(grade_number=gradeToTeach).first()
        self.class_teacher = value

    def __repr__(self):
        return f'<Staff {self.username}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(36), index = True)
    market_value = db.Column(db.Integer)
    publisher_name = db.Column(db.String(36))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable= False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(24), index = True)
    last_name = db.Column(db.String(24))
    username = db.Column(db.String(24), unique = True)
    address = db.Column(db.Text(length = 100))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'




@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
