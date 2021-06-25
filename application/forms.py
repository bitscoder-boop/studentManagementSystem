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
    classList = [i.grade_number for i in Grade.query.all()] # get all class names i.e. grade_number
    classList = [ (i, i) for i in classList] # generate select options list
    username = StringField('Assign Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators = [DataRequired()])
    middle_name = StringField('Middle Name',validators = [Optional()] )
    last_name = StringField('Last Name', validators = [DataRequired()])
    gender = SelectField('Gender', choices = [('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    email = StringField('Email', validators = [Optional(), Email()])
    contact = IntegerField('Phone', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    current_grade = SelectField('Current Class', choices=classList, validators=[DataRequired()])
    submit = SubmitField('Add Student')

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        if len(username.data) < 5:
            raise ValidationError('Use longer name')


class AddStaffForm(FlaskForm):
    classList = [i.grade_number for i in Grade.query.filter_by(classteachers=None).all()] # get all class names i.e. grade_number
    classList = [ (i, i) for i in classList] # generate select options list
    classList.insert(0, (None, 'Select One'))
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
    class_teacher = SelectField('Class Teacher Of', choices = classList, validators=[Optional()])
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


    def validate_contact(self, contact):
        contact_number = contact.data
        if type(contact_number) != int:
            raise ValidationError('Phone Number should be numeric value')

        elif len(str(contact_number)) != 10:
            raise ValidationError('Phone Number are supposed to be 10 digits.')


class editStaffForm(FlaskForm): 
    classList = [i.grade_number for i in Grade.query.filter_by(classteachers=None).all()] # get all class names i.e. grade_number
    classList = [ (i, i) for i in classList] # generate select options list
    classList.insert(0, (None, 'Select One'))

    first_name = StringField('First Name', validators = [DataRequired()])
    middle_name = StringField('Middle Name',validators = [Optional()] )
    last_name = StringField('Last Name', validators = [DataRequired()])
    gender = SelectField('Gender', choices = [('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    contact = IntegerField('Phone', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired(message = "Enter valid Phone Number")])
    class_teacher = SelectField('Class Teacher Of', choices = classList, validators=[Optional()])

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



    def validate_grade_number(self, grade_number):
        value = grade_number.data
        classValueFromDatabase = Grade.query.filter_by(grade_number=value).first()
        if classValueFromDatabase is not None:
            raise ValidationError('Given class is already present in databse.')

