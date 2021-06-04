from application import app, db
from application.models import Grade, Student, Staff, Subject

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Grade': Grade, 'Student': Student, 'Staff': Staff, 'Subject': Subject}
