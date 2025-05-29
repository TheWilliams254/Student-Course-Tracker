from app.models import Student, Course, Enrollment, Assignment, engine, Base, Teacher
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
    print("3. Enroll Student in Course")
    print("4. Add Assignment")
    print("5. List Assignments")
    print("6. Mark Assignment as Submitted")
    print("0. Logout")

def student_menu():
    print("\n=== Student Menu ===")
    print("1. View My Courses")
    print("2. View My Assignments")
    print("0. Logout")

# ------------------ Teacher Actions ------------------

def add_student():
    first = input("First Name: ")
    last = input("Last Name: ")
    email = input("Email: ")
    gpa = float(input("GPA: "))

    student = Student(first_name=first, last_name=last, email=email, gpa=gpa)
    session.add(student)
    session.commit()
    print(f"✅ Student {first} {last} added.")

def add_course():
    name = input("Course Name: ")
    code = input("Course Code: ")
    semester = input("Semester: ")

    course = Course(name=name, code=code, semester=semester)
    session.add(course)
    session.commit()
    print(f"✅ Course {name} added.")

def enroll_student():
    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    session.add(enrollment)
    session.commit()
    print(f"✅ Student {student_id} enrolled in course {course_id}.")

def add_assignment():
    title = input("Assignment Title: ")
    due_str = input("Due Date (YYYY-MM-DD): ")
    due_date = datetime.strptime(due_str, "%Y-%m-%d")
    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    
    assignment = Assignment(
        title=title,
        due_date=due_date,
        submitted=False,
        student_id=student_id,
        course_id=course_id
    )
    session.add(assignment)
    session.commit()
    print(f"✅ Assignment '{title}' added.")

def list_assignments():
    assignments = session.query(Assignment).all()
    for a in assignments:
        status = "✅" if a.submitted else "❌"
        print(f"[{status}] {a.title} | Due: {a.due_date.date()} | Student ID: {a.student_id}")

def mark_submitted():
    assignment_id = int(input("Assignment ID to mark as submitted: "))
    assignment = session.query(Assignment).get(assignment_id)
    if assignment:
        assignment.submitted = True
        session.commit()
        print("✅ Assignment marked as submitted.")
    else:
        print("❌ Assignment not found.")

# ------------------ Main ------------------

def main():
    while True:
        role = choose_role()
        
        if role == "1":  # Teacher
            teacher = teacher_login()
            if not teacher:
                continue #return to main menu
            while True:
                teacher_menu()
                choice = input("Enter choice: ")
                if choice == "1":
                    add_student()
                elif choice == "2":
                    add_course()
                elif choice == "3":
                    enroll_student()
                elif choice == "4":
                    add_assignment()
                elif choice == "5":
                    list_assignments()
                elif choice == "6":
                    mark_submitted()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice.")

        elif role == "2":  # Student
            student_id = int(input("Enter your Student ID: "))
            while True:
                student_menu()
                choice = input("Enter choice: ")
                if choice == "1":
                    courses = session.query(Course).join(Enrollment).filter(Enrollment.student_id == student_id).all()
                    print("\nYour Courses:")
                    for c in courses:
                        print(f"- {c.name} ({c.code})")
                elif choice == "2":
                    assignments = session.query(Assignment).filter(Assignment.student_id == student_id).all()
                    print("\nYour Assignments:")
                    for a in assignments:
                        status = "✅ Submitted" if a.submitted else "❌ Pending"
                        print(f"- {a.title} | Due: {a.due_date.date()} | {status}")
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
