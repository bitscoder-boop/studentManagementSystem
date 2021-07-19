from .import app
from application import db
from .forms import LoginForm, AddStudentForm, AddStaffForm, addClassForm, editStaffForm, editClassForm
from .models import Admin, Student, Staff, Grade, Subject 
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, url_for, request, redirect, flash

@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    '''handle admin login'''
    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form.get('username')).first() # return username if avilable else none
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


@app.route('/addStaff', methods = ['GET', 'POST'])
def add_staff():
    '''handle the form that create staff'''
    form = AddStaffForm()
    if form.validate_on_submit(): # csrf token must be available 
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
        db.session.add(user) # uncomment on production
        db.session.commit()
        flash('Succesfully added staff.')
        return redirect(url_for('manageStaff'))
    return render_template('hod_templates/staff/addStaff.html', form=form)
# this is comment


@app.route('/manageStaff')
def manageStaff():
    '''responsible to show the table contaning all staff data'''
    teacherData = Staff.query.all()
    return render_template('hod_templates/staff/manageStaff.html', teacherData = teacherData)


@app.route('/editStaff/<username>', methods=["GET", "POST"])
def editStaff(username):
    '''edit profile of each staff'''
    currentStaff = Staff.query.filter_by(username=username).first()
    form = editStaffForm(value = currentStaff)
    if form.validate_on_submit(): #request.method == "POST":
        currentStaff.first_name = form.first_name.data
        currentStaff.middle_name = form.middle_name.data
        currentStaff.last_name = form.last_name.data
        currentStaff.gender = form.gender.data
        currentStaff.contact = int(form.contact.data)
        currentStaff.address = form.address.data    
        if form.class_teacher.data:
            currentStaff.assign_classTeaching(form.class_teacher.data)
        db.session.commit() 
        flash('Succesfully Edited')
        return redirect(url_for('manageStaff'))
    if request.method == "GET": # prepopulate the form
        form.first_name.data = currentStaff.first_name
        form.middle_name.data = currentStaff.middle_name
        form.last_name.data = currentStaff.last_name
        form.gender.data = currentStaff.gender
        form.contact.data = currentStaff.contact
        form.address.data = currentStaff.address
    return render_template('hod_templates/staff/editStaff.html', form=form, username=username)



@app.route('/deleteStaff/<username>', methods=["GET", "POST"])
def deleteStaff(username):
    '''delete the staff with given username'''
    data = Staff.query.filter_by(username=username)
    data.delete()
    db.session.commit()
    flash(f'{username} deleted succesfullt')
    return redirect(url_for('manageStaff'))


##############################################
########Class#################################
##############################################

@app.route('/manageClass')
def manageClass():
    classData = Grade.query.all()
    return render_template('hod_templates/class/manageClass.html', classData = classData)


@app.route('/addClass', methods = ['GET', 'POST'])
def addClass():
    '''handle form that assign total subject and class teacher to each class'''
    form = addClassForm()
    if form.validate_on_submit():
        value = Grade(
                grade_number = form.grade_number.data.lower(),
                total_subject = form.total_subject_count.data,
                )
        if form.class_teacher.data:
            value.assign_classTeacher(form.class_teacher.data)
        db.session.add(value) # uncomment in production
        db.session.commit()
        flash('Succesfully added class.')
        return redirect(url_for('manageClass'))
    return render_template('hod_templates/class/addClass.html', form=form)


@app.route('/editClass/<id>', methods = ['GET', 'POST'])
def editClass(id):
    g = Grade.query.get(id)
    form = editClassForm(value=g)
    if form.validate_on_submit():
        g.grade_number = form.grade_number.data.lower()
        g.total_subject = form.total_subject_count.data
        if form.class_teacher.data == 'None':
            g.classteachers = None
        else:
            g.classteachers = Staff.query.filter_by(username=str(form.class_teacher.data)).first()
        db.session.commit()
        flash('Succesfully added class.')
        return redirect(url_for('manageClass'))
    if request.method == 'GET':
        form.grade_number.data = g.grade_number
        form.total_subject_count.data = g.total_subject
    return render_template('hod_templates/class/editClass.html', form=form) 


@app.route('/deleteClass/<id>')
def deleteClass(id):
    grade_to_delete = Grade.query.filter_by(id=id)
    grade_to_delete.delete()
    db.session.commit()
    flash('Succesfully Deleted')
    return redirect(url_for('manageClass'))


##############################################
####################SUBJECT###################
##############################################

@app.route('/manageSubjects', methods = ['GET', 'POST'])
def manageSubjects():
    ''' responsible to handle the form that change grade to add differnt subject'''
    #if request.method == "POST":
        #className = request.form.get('searchClass')
        #return redirect(url_for('updateClassDetails', className=className))
    classList = [i for i in Grade.query.all() if len(i.subjects) > 0] # get class grade name
    return render_template('hod_templates/subjects/manageSubjects.html', classList = classList, currentClass = 'Select One')


@app.route('/addSubjects/<className>', methods = ['GET', 'POST'])
def updateClassDetails(className):
    '''add subject, subject Teacher to the given class''' 
    TeacherList = [i.username for i in Staff.query.all()]
    classList = [i.grade_number for i in Grade.query.all()] # get class grade name
    currentClass = className
    try:
        total_subject = Grade.query.filter_by(grade_number=className).first().total_subject
    except AttributeError:
        '''if total_subject of current class return error'''
        return render_template('500.html', message="Make sure given class got subject number assigned", passForm = True, classList= classList)
    if request.method == 'POST':
        grade = Grade.query.filter_by(grade_number=currentClass).first()
        for i in range(total_subject):
            name = request.form.get('subject' +str(i))
            market_value = request.form.get('price' + str(i))
            publisher_name = request.form.get('publisher' + str(i))
            s = Subject(name = name,
                    market_value = market_value,
                    publisher_name = publisher_name,
                    grade = grade)
            if request.form.get('teacher' + str(i)) is not None:
                print(request.form.get('teacher' + str(i)))
                teacher = Staff.query.filter_by(username=request.form.get('teacher' + str(i))).first()
                s.teacher.append(teacher)
            else:
                print('Null')
            db.session.add(s)
        db.session.commit() #uncomment in production 
        flash('Succesfully added', 'message')
    return render_template('hod_templates/update_class.html', total_subject = total_subject, myTeacherList=TeacherList, classList = classList, currentClass = currentClass)


@app.route('/manageStudent')
def manageStudent():
    return render_template('hod_templates/manageStudentHPage.html')

@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():
    form = AddStudentForm()
    if form.validate_on_submit(): #csrf token must be avilable
        s = Student(username = form.username.data,
                first_name = form.first_name.data,
                middle_name = form.middle_name.data,
                last_name = form.last_name.data,
                gender = form.gender.data,
                address = form.address.data,
                email = form.email.data,
                contact = form.contact.data,
                grade = Grade.query.filter_by(grade_number = form.current_grade.data).first()
                )
        s.set_password(form.password.data)
        db.session.add(s)
        db.session.commit()
        flash('Succesfully added student')
    return render_template('hod_templates/addStudentHPage.html', form=form)
