from .import app
from application import db
from .forms import LoginForm, AddStudentForm, AddStaffForm, ManageClassForm
from .models import Admin, Student, Staff, Grade, Subject 
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, url_for, request, redirect, flash

@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form.get('username')).first()
        if admin is None or not admin.check_password(request.form.get('password')):
            flash('Invalid username or password')
            return redirect(url_for('admin_login'))
        login_user(admin, remember = request.form.get('remember_me'))
        return redirect(url_for('adminHomePage'))
    return render_template('login_page.html')

@app.route('/admin_logout')
def admin_logout():
    logout_user()
    return redirect(url_for('showDemoPage'))

@app.route('/demo')
def showDemoPage():
    return render_template('demo.html')


@app.route('/admin_home')
def adminHomePage():
    return render_template('hod_templates/home_content.html')


@app.route('/add_staff', methods = ['GET', 'POST'])
def add_staff():
    form = AddStaffForm()
    if form.validate_on_submit():
        user = Staff(
        first_name = form.first_name.data,
        middle_name = form.middle_name.data,
        last_name = form.last_name.data,
        username = form.username.data,
        gender = form.gender.data,
        address = form.address.data,
        email = form.email.data,
        contact = int(form.contact.data)
        )
        user.set_password(form.password.data)
        if form.class_teacher.data:
            user.assign_classTeaching(form.class_teacher.data)
        db.session.add(user)
        db.session.commit()
        flash('Succesfully added staff.')
    return render_template('hod_templates/add_staff_template.html', form=form)


@app.route('/manage_class', methods = ['GET', 'POST'])
def manageClass():
    form = ManageClassForm()
    if form.validate_on_submit():
        value = Grade(
        grade_number = form.grade_number.data.lower(),
        total_subject = form.total_subject_count.data,
        )
        if form.class_teacher.data:
            value.assign_classTeacher(form.class_teacher.data)
        db.session.add(value)
        db.session.commit()
        flash('Succesfully added class.')
    return render_template('hod_templates/manage_class.html', form=form)

@app.route('/update_class/<className>', methods = ['GET', 'POST'])
def updateClassDetails(className):
    TeacherList = [i.username for i in Staff.query.filter_by(grade_subject=None).all()]
    classList = [i.grade_number for i in Grade.query.all()] # get class grade name
    currentClass = className
    print(classList)
    try:
        total_subject = Grade.query.filter_by(grade_number=className).first().total_subject
    except AttributeError:
        '''if total_subject of current class return error'''
        return render_template('500.html', message="Make sure given class got subject number assigned", passForm = True, classList= classList)
    if request.method == 'POST':
        subjectList = [] # get the list of subject name from the form
        subjectTeacherList = []
        marketPriceList = []
        publisherNameList = []
        grade = Grade.query.filter_by(grade_number=currentClass).first()
        for i in range(total_subject):
            name = request.form.get('subject' +str(i))
            market_value = request.form.get('price' + str(i))
            publisher_name = request.form.get('publisher' + str(i))
            teacher = Staff.query.filter_by(username=request.form.get('teacher' + str(i))).first()
            s = Subject(name = name,
                        market_value = market_value,
                        publisher_name = publisher_name,
                        grade = grade,
                        teacher = teacher)
            db.session.add(s)
        #db.session.commit()
        flash('Succesfully added', 'message')
    return render_template('hod_templates/update_class.html', total_subject = total_subject, myTeacherList=TeacherList, classList = classList, currentClass = currentClass)

@app.route('/updateClass', methods=["GET", "POST"])
def updateClass():
    if request.method == "POST":
        className = request.form.get('searchClass')
        print(className)
    return redirect(url_for('updateClassDetails', className=className))
