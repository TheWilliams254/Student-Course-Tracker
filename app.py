from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Student, Enrollment, Course, Assignment, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for flash messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        reg_no = request.form['registration_number'].strip()
        student = session.query(Student).filter_by(registration_number=reg_no).first()
        if student:
            return redirect(url_for('student_dashboard', reg_no=reg_no))
        flash("Invalid registration number.", "error")
    return render_template('student_login.html')

@app.route('/student/<reg_no>')
def student_dashboard(reg_no):
    student = session.query(Student).filter_by(registration_number=reg_no).first()
    if not student:
        return f"<h2>Student with reg no {reg_no} not found.</h2>", 404
    courses = session.query(Course).join(Enrollment).filter(Enrollment.student_id == student.id).all()
    assignments = session.query(Assignment).filter(Assignment.student_id == student.id).all()
    return render_template('student_dashboard.html', student=student, courses=courses, assignments=assignments)

@app.route('/teacher-dashboard')
def teacher_dashboard():
    students = session.query(Student).all()
    courses = session.query(Course).all()
    return render_template('teacher_dashboard.html', students=students, courses=courses)

@app.route('/add-assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        title = request.form['title']
        due_date_str = request.form['due_date']
        course_id = request.form['course_id']
        reg_no = request.form['reg_no'].strip()

        student = session.query(Student).filter_by(registration_number=reg_no).first()
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('add_assignment'))
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('add_assignment'))

        assignment = Assignment(
            title=title,
            due_date=due_date,
            submitted=False,
            student_id=student.id,
            course_id=course_id
        )
        session.add(assignment)
        session.commit()
        flash('Assignment added successfully.', 'success')
        return redirect(url_for('teacher_dashboard'))
    
    courses = session.query(Course).all()
    return render_template('add_assignment.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)
