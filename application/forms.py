from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, EqualTo, Email, NumberRange, InputRequired, ValidationError, Regexp
from application.models import Staff, Grade
from flask import request 

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddStudentForm(FlaskForm):
    username = StringField('Assign Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired()])
    middle_name = StringField('Middle Name',validators = [Optional()] )
    last_name = StringField('Last Name', validators = [DataRequired()])
    gender = SelectField('Gender', choices = [('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    current_grade = StringField('Class', validators = [DataRequired()])
    submit = SubmitField('Add Student')

class AddStaffForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message = 'Required Field')])
    first_name = StringField('First Name', validators = [DataRequired()])
    middle_name = StringField('Middle Name',validators = [Optional()] )
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    gender = SelectField('Gender', choices = [('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    contact = IntegerField('Phone', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired(message = "Enter valid Phone Number")])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    class_teacher = StringField('ClassTeacher', validators = [Optional()])
    submit = SubmitField('Add Staff')

    def validate_username(self, username):
        user = Staff.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        if len(username.data) < 5:
            raise ValidationError('Use longer name')

    def validate_email(self, email):
        user = Staff.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_class_teacher(self, class_teacher):
        grade = Grade.query.filter_by(grade_number=class_teacher.data).first()
        if grade is None:
            raise ValidationError('Enter a valid class. Make sure your class is present in Database.')
        elif grade.classteachers:
            raise ValidationError('ClassTeacher already assign for current class. Remove it first')

    def validate_contact(self, contact):
        contact_number = contact.data
        if type(contact_number) != int:
            raise ValidationError('Phone Number should be numeric value')

        elif len(str(contact_number)) != 10:
            raise ValidationError('Phone Number are supposed to be 10 digits.')


class ManageClassForm(FlaskForm):
    regexMessage = 'AlphaNumeric and Numeric Value not accepted!'

    teacher_list = Staff.query.filter_by(class_teacher=None).all()
    teacherselectList = [(x.username, x.username) for x in teacher_list]
    teacherselectList.append(('', 'Select Later'))

    grade_number = StringField('Class', validators=[DataRequired(), Regexp("^\D+$", message = regexMessage)])
    total_subject_count = IntegerField('Total Subject', validators=[DataRequired()])
    class_teacher = SelectField('ClassTeacher Name', choices = teacherselectList, default = '' , validators=[Optional()])
    submit = SubmitField('Add Class')

    def validate_class_teacher(self, class_teacher):
        value = Staff.query.filter_by(username=class_teacher.data).first()
        gradeNotassignedList = Staff.query.filter_by(class_teacher=None).all()
        if value is None:
            raise ValidationError('Teacher not registered. Register it first')
        elif class_teacher.data not in gradeNotassignedList:
            raise ValidationError('Cannot assign class teacher to current class.\nGiven teacher already got class teaching post.')
            # admin have assigned given teacher to some class as class teacher.


    def validate_grade_number(self, grade_number):
        value = grade_number.data
        classValueFromDatabase = Grade.query.filter_by(grade_number=value).first()
        if classValueFromDatabase is not None:
            raise ValidationError('Given class is already present in databse.')

