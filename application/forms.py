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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_teacher.choices = [
                (i.grade_number , i.grade_number) for i in Grade.query.filter_by(classteachers=None).all()
                ]
        self.class_teacher.choices.insert(0, (None, 'Select Later'))

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
    class_teacher = SelectField('Class Teacher Of', validators=[Optional()])
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
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_teacher.choices = [
                (i.grade_number, i.grade_number) for i in Grade.query.filter_by(classteachers=None).all()
                ]
        if value.class_teacher:
            self.class_teacher.choices.insert(0, (value.class_teacher.grade_number, value.class_teacher.grade_number))
            self.class_teacher.choices.insert(1, (None, 'Select Later'))
        else:
            self.class_teacher.choices.insert(0, (None, 'Select Later'))

    classList = [i.grade_number for i in Grade.query.filter_by(classteachers=None).all()] # get all class names i.e. grade_number

    first_name = StringField('First Name', validators = [DataRequired()])
    middle_name = StringField('Middle Name',validators = [Optional()] )
    last_name = StringField('Last Name', validators = [DataRequired()])
    gender = SelectField('Gender', choices = [('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    contact = IntegerField('Phone', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired(message = "Enter valid Phone Number")])
    class_teacher = SelectField('Class Teacher Of', validators=[Optional()])

    def validate_contact(self, contact):
        contact_number = contact.data
        if type(contact_number) != int:
            raise ValidationError('Phone Number should be numeric value')

        elif len(str(contact_number)) != 10:
            raise ValidationError('Phone Number are supposed to be 10 digits.')




class addClassForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_teacher.choices = [(x.username, x.username) for x in Staff.query.filter_by(class_teacher=None).all()]
        self.class_teacher.choices.insert(0, (None, 'Select Later'))

    regexMessage = 'AlphaNumeric and Numeric Value not accepted!'
    grade_number = StringField('Class', validators=[DataRequired(), Regexp("^\D+$", message = regexMessage)])
    total_subject_count = IntegerField('Total Subject', validators=[DataRequired()])
    class_teacher = SelectField('ClassTeacher Name', validators=[Optional()])
    submit = SubmitField('Add Class')



class editClassForm(FlaskForm):
    def __init__(self, value,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_teacher.choices = [(x.username, x.username) for x in Staff.query.filter_by(class_teacher=None).all()]
        if value.classteachers:
            self.class_teacher.choices.insert(0, (value.classteachers.username, value.classteachers.username))
            self.class_teacher.choices.insert(1, (None, 'Select Later'))
        else:
            self.class_teacher.choices.insert(0, (None, 'Select Later'))

    regexMessage = 'AlphaNumeric and Numeric Value not accepted!'
    grade_number = StringField('Class', validators=[DataRequired(), Regexp("^\D+$", message = regexMessage)])
    total_subject_count = IntegerField('Total Subject', validators=[DataRequired()])
    class_teacher = SelectField('ClassTeacher Name', validators=[Optional()])
    submit = SubmitField('Add Class')

