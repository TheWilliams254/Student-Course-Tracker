from models import Student, Course, Enrollment, Assignment, engine, Base, Teacher
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()
import hashlib

#Teacher's Login Authentication
def teacher_login():
    email = input("Email: ")
    password = input("Password: ")
    teacher = session.query(Teacher).filter_by(email=email).first()
    if teacher and teacher.check_password(password):
        print(f"✅ Welcome, {teacher.name}!")
        return teacher
    else:
        print("❌ Invalid credentials.")
        return None
# ------------------ Menus ------------------

def choose_role():
    print("\nWelcome to Student Course Tracker!")
    print("1. Teacher")
    print("2. Student")
    print("0. Exit")
    return input("Choose your role: ")

def teacher_menu():
    print("\n=== Teacher Menu ===")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enroll Students in Course")  
    print("4. Add Assignment for One Student")
    print("5. Add Assignment to Entire Course") 
    print("6. List Assignments")
    print("7. Mark Assignment as Submitted")
    print("8. View All Students")
    print("0. Logout")


def student_menu():
    print("\n=== Student Menu ===")
    print("1. View My Courses")
    print("2. View My Assignments")
    print("0. Logout")

# ------------------ Teacher Actions ------------------

def add_student():
    reg_no = input("Registration Number: ").strip()
    first = input("First Name: ")
    last = input("Last Name: ")
    email = input("Email: ")
    gpa = float(input("GPA: "))

    student = Student(
        registration_number=reg_no,
        first_name=first,
        last_name=last,
        email=email,
        gpa=gpa
    )
    session.add(student)
    try:
        session.commit()
        print(f"✅ Student {first} {last} added.")
    except:
        session.rollback()
        print("❌ Error: Possibly duplicate registration number or email.")
def add_course():
    name = input("Course Name: ")
    code = input("Course Code: ")
    semester = input("Semester: ")

    course = Course(name=name, code=code, semester=semester)
    session.add(course)
    session.commit()
    print(f"✅ Course {name} added.")

def enroll_students():
    course_id = int(input("Course ID: "))
    reg_nos = input("Enter registration numbers (comma-separated): ").split(',')

    enrolled_count = 0
    for reg_no in reg_nos:
        reg_no = reg_no.strip()
        student = session.query(Student).filter_by(registration_number=reg_no).first()
        if not student:
            print(f"❌ Student with reg no '{reg_no}' not found.")
            continue
        
        already_enrolled = session.query(Enrollment).filter_by(student_id=student.id, course_id=course_id).first()
        if already_enrolled:
            print(f"ℹ️ Student {reg_no} is already enrolled.")
            continue

        enrollment = Enrollment(student_id=student.id, course_id=course_id)
        session.add(enrollment)
        enrolled_count += 1

    session.commit()
    print(f"✅ Enrolled {enrolled_count} students in course {course_id}.")


def add_assignment():
    title = input("Assignment Title: ")
    due_str = input("Due Date (YYYY-MM-DD): ")
    due_date = datetime.strptime(due_str, "%Y-%m-%d")
    reg_no = input("Student Registration Number: ").strip().upper()
    course_id = int(input("Course ID: "))

    student = session.query(Student).filter_by(registration_number=reg_no).first()
    if not student:
        print("❌ Student not found.")
        return

    assignment = Assignment(
        title=title,
        due_date=due_date,
        submitted=False,
        student_id=student.id,
        course_id=course_id
    )
    session.add(assignment)
    session.commit()
    print(f"✅ Assignment '{title}' added for {reg_no}.")
def add_assignment_to_course():
    title = input("Assignment Title: ")
    due_str = input("Due Date (YYYY-MM-DD): ")
    due_date = datetime.strptime(due_str, "%Y-%m-%d")
    course_id = int(input("Course ID: "))

    enrollments = session.query(Enrollment).filter_by(course_id=course_id).all()
    if not enrollments:
        print("❌ No students enrolled in this course.")
        return

    for enrollment in enrollments:
        assignment = Assignment(
            title=title,
            due_date=due_date,
            submitted=False,
            student_id=enrollment.student_id,
            course_id=course_id
            )
        session.add(assignment)

        session.commit()
        print(f"✅ Assignment '{title}' added for all enrolled students in course {course_id}.")

        session.add(assignment)
        session.commit()
        print(f"✅ Assignment '{title}' added for all students.")

def list_assignments():
    assignments = session.query(Assignment).all()
    for a in assignments:
        status = "✅" if a.submitted else "❌"
        student = session.get(Student, a.student_id)
        print(f"[{status}] {a.title} | Due: {a.due_date.date()} | Student: {student.registration_number} ({student.first_name} {student.last_name})")

def mark_submitted():
    assignment_id = int(input("Assignment ID to mark as submitted: "))
    assignment = session.query(Assignment).get(assignment_id)
    if assignment:
        assignment.submitted = True
        session.commit()
        print("✅ Assignment marked as submitted.")
    else:
        print("❌ Assignment not found.")
def view_all_students():
    students = session.query(Student).all()
    if not students:
        print("❌ No students found.")
        return
    print("\n=== Student List ===")
    for student in students:
        print(f"Reg No: {student.registration_number} | Name: {student.first_name} {student.last_name} | Email: {student.email} | GPA: {student.gpa}")
    print("=== End of Student List ===")

# ------------------ Main ------------------

def main():
    while True:
        role = choose_role()

        if role == "1":  # Teacher
            teacher = teacher_login()
            if not teacher:
                continue  # return to main menu

            while True:
                teacher_menu()
                choice = input("Enter choice: ")
                if choice == "1":
                    add_student()
                elif choice == "2":
                    add_course()
                elif choice == "3":
                    enroll_students()
                elif choice == "4":
                    add_assignment()
                elif choice == "5":
                    add_assignment_to_course()
                elif choice == "6":
                    list_assignments()
                elif choice == "7":
                    mark_submitted()
                elif choice == "8":
                    view_all_students()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice.")

        elif role == "2":  # Student
            reg_no = input("Enter your Registration Number: ").strip().upper()
            student = session.query(Student).filter_by(registration_number=reg_no).first()

            if not student:
                print("❌ Student not found.")
                continue

            while True:
                student_menu()
                choice = input("Enter choice: ")
                if choice == "1":
                    # Show student's enrolled courses
                    courses = session.query(Course).join(Enrollment).filter(Enrollment.student_id == student.id).all()
                    if not courses:
                        print("⚠️  No enrolled courses found.")
                    else:
                        print("Your Courses:")
                        for c in courses:
                            print(f"- {c.name} ({c.code})")
                elif choice == "2":
                    # Show student's assignments
                    assignments = session.query(Assignment).filter(Assignment.student_id == student.id).all()
                    if not assignments:
                        print("⚠️  No assignments found.")
                    else:
                        print("Your Assignments:")
                        for a in assignments:
                            status = "✅" if a.submitted else "❌"
                            print(f"[{status}] {a.title} | Due: {a.due_date.strftime('%Y-%m-%d')}")
                elif choice == "0":
                    break
                else:
                    print("Invalid choice.")

        elif role == "0":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid role choice.")

if __name__ == "__main__":
    main()

