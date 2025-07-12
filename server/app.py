from flask import Flask, render_template, request, redirect, url_for, session, flash
from .models import Student, Teacher, Course, Assignment, Enrollment, engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

Session = sessionmaker(bind=engine)
db_session = Session()

# ----- Decorators -----
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'teacher_id' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('teacher_login'))
        return f(*args, **kwargs)
    return decorated_function

# ----- Routes -----

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        teacher = db_session.query(Teacher).filter_by(email=email).first()
        if teacher and teacher.check_password(password):
            session['teacher_id'] = teacher.id
            flash(f"Welcome, {teacher.name}!", "success")
            return redirect(url_for('teacher_dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('teacher_login'))

    return render_template('teacher_login.html')

@app.route('/teacher/logout')
@login_required
def teacher_logout():
    session.pop('teacher_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('teacher_login'))

@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    teacher = db_session.query(Teacher).get(session['teacher_id'])
    students = db_session.query(Student).all()
    courses = db_session.query(Course).all()
    assignments = db_session.query(Assignment).all()
    return render_template(
        'teacher_dashboard.html',
        teacher=teacher,
        students=students,
        courses=courses,
        assignments=assignments
    )

@app.route('/teacher/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        reg_no = request.form['registration_number'].strip()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gpa = float(request.form['gpa'])

        if db_session.query(Student).filter_by(registration_number=reg_no).first():
            flash("Student with this registration number already exists.", "danger")
            return redirect(url_for('add_student'))

        student = Student(
            registration_number=reg_no,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gpa=gpa
        )
        db_session.add(student)
        db_session.commit()
        flash(f"Student {first_name} {last_name} added successfully.", "success")
        return redirect(url_for('teacher_dashboard'))
    return render_template('add_student.html')

@app.route('/teacher/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        semester = request.form['semester']

        if db_session.query(Course).filter_by(code=code).first():
            flash("Course with this code already exists.", "danger")
            return redirect(url_for('add_course'))

        course = Course(name=name, code=code, semester=semester)
        db_session.add(course)
        db_session.commit()
        flash(f"Course '{name}' added successfully.", "success")
        return redirect(url_for('teacher_dashboard'))
    return render_template('add_course.html')

@app.route('/teacher/enroll_students', methods=['GET', 'POST'])
@login_required
def enroll_students():
    courses = db_session.query(Course).all()
    if request.method == 'POST':
        course_id = int(request.form['course_id'])
        reg_nos = request.form['registration_numbers'].split(',')

        enrolled_count = 0
        for reg_no in reg_nos:
            reg_no = reg_no.strip()
            student = db_session.query(Student).filter_by(registration_number=reg_no).first()
            if not student:
                flash(f"Student with reg no '{reg_no}' not found.", "warning")
                continue
            already_enrolled = db_session.query(Enrollment).filter_by(student_id=student.id, course_id=course_id).first()
            if already_enrolled:
                flash(f"Student {reg_no} is already enrolled.", "info")
                continue

            enrollment = Enrollment(student_id=student.id, course_id=course_id)
            db_session.add(enrollment)
            enrolled_count += 1

        db_session.commit()
        flash(f"Enrolled {enrolled_count} students in course.", "success")
        return redirect(url_for('teacher_dashboard'))
    return render_template('enroll_students.html', courses=courses)

@app.route('/teacher/add_assignment', methods=['GET', 'POST'])
@login_required
def add_assignment():
    courses = db_session.query(Course).all()
    if request.method == 'POST':
        title = request.form['title']
        due_date_str = request.form['due_date']
        reg_no = request.form['registration_number'].strip()
        course_id = int(request.form['course_id'])

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return redirect(url_for('add_assignment'))

        student = db_session.query(Student).filter_by(registration_number=reg_no).first()
        if not student:
            flash("Student not found.", "danger")
            return redirect(url_for('add_assignment'))

        assignment = Assignment(
            title=title,
            due_date=due_date,
            submitted=False,
            student_id=student.id,
            course_id=course_id
        )
        db_session.add(assignment)
        db_session.commit()
        flash(f"Assignment '{title}' added for {reg_no}.", "success")
        return redirect(url_for('teacher_dashboard'))
    return render_template('add_assignment.html', courses=courses)

@app.route('/teacher/add_assignment_course', methods=['GET', 'POST'])
@login_required
def add_assignment_course():
    courses = db_session.query(Course).all()
    if request.method == 'POST':
        title = request.form['title']
        due_date_str = request.form['due_date']
        course_id = int(request.form['course_id'])

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return redirect(url_for('add_assignment_course'))

        enrollments = db_session.query(Enrollment).filter_by(course_id=course_id).all()
        if not enrollments:
            flash("No students enrolled in this course.", "warning")
            return redirect(url_for('add_assignment_course'))

        for enrollment in enrollments:
            assignment = Assignment(
                title=title,
                due_date=due_date,
                submitted=False,
                student_id=enrollment.student_id,
                course_id=course_id
            )
            db_session.add(assignment)
        db_session.commit()
        flash(f"Assignment '{title}' added for all students in course.", "success")
        return redirect(url_for('teacher_dashboard'))

    return render_template('add_assignment_course.html', courses=courses)

@app.route('/teacher/list_assignments')
@login_required
def list_assignments():
    assignments = db_session.query(Assignment).all()
    return render_template('list_assignments.html', assignments=assignments)

@app.route('/teacher/mark_submitted/<int:assignment_id>')
@login_required
def mark_submitted(assignment_id):
    assignment = db_session.query(Assignment).get(assignment_id)
    if assignment:
        assignment.submitted = True
        db_session.commit()
        flash("Assignment marked as submitted.", "success")
    else:
        flash("Assignment not found.", "danger")
    return redirect(url_for('list_assignments'))

@app.route('/teacher/view_students')
@login_required
def view_all_students():
    students = db_session.query(Student).all()
    return render_template('view_students.html', students=students)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        reg_no = request.form['registration_number']
        # password = request.form['password']

        student = db_session.query(Student).filter_by(registration_number=reg_no).first()
        if student:
            session['student_id'] = student.id
            flash(f"Welcome {student.first_name}!", "success")
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid registration number or password.", "danger")
    return render_template('student_login.html')

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('student_login'))

def student_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash("Please log in as student.", "warning")
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/student/dashboard')
@student_login_required
def student_dashboard():
    student = db_session.query(Student).get(session['student_id'])
    enrollments = db_session.query(Enrollment).filter_by(student_id=student.id).all()
    assignments = db_session.query(Assignment).filter_by(student_id=student.id).all()
    return render_template('student_dashboard.html', student=student, enrollments=enrollments, assignments=assignments)


if __name__ == '__main__':
    app.run(debug=True)
