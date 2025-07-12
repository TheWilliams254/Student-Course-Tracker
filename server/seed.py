from models import Base, engine, Teacher, Student, Course, Enrollment, Assignment
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

# Drop and recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# ---------------------------
# Add Default Teacher Only
# ---------------------------
def default_teacher():
    if session.query(Teacher).count() == 0:
        teacher = Teacher(name="William", email="william@example.com")
        teacher.set_password("William@Hawks;")
        session.add(teacher)
        session.commit()
        print("✅ Added default teacher.")

default_teacher()

# ---------------------------
# Add Students
# ---------------------------
first_names = ["Liam", "Emma", "Noah", "Olivia", "Elijah", "Ava", "James", "Sophia", "Lucas", "Isabella", "Mason", "Mia", "Ethan", "Amelia", "Logan"]
last_names = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Lee", "Walker", "Hall", "Allen", "Young"]

students = []
for i in range(15):
    reg_no = f"S20{i:02d}"
    student = Student(
        registration_number=reg_no,
        first_name=first_names[i],
        last_name=last_names[i],
        email=f"{first_names[i].lower()}.{last_names[i].lower()}@example.com",
        gpa=round(random.uniform(2.5, 4.0), 2)
    )
    students.append(student)

# ---------------------------
# Add Courses
# ---------------------------
course_names = [
    ("Software Engineering", "SE101"),
    ("Data Science", "DS102"),
    ("Cyber Security", "CS103"),
    ("Database Systems", "DB104"),
    ("Artificial Intelligence", "AI105")
]
courses = [Course(name=name, code=code, semester="Fall 2025") for name, code in course_names]

# ---------------------------
# Enroll Students in 2 Random Courses Each
# ---------------------------
enrollments = []
for student in students:
    enrolled_courses = random.sample(courses, k=2)
    for course in enrolled_courses:
        enrollments.append(Enrollment(student=student, course=course))

# ---------------------------
# Add Assignments for Enrollments
# ---------------------------
assignments = []
sample_titles = ["Project Proposal", "Midterm Quiz", "Final Exam", "Group Work", "Lab Report"]
due_dates = [datetime(2025, 6, 5), datetime(2025, 6, 15), datetime(2025, 7, 1)]

for enrollment in enrollments:
    for title in random.sample(sample_titles, 2):
        assignments.append(
            Assignment(
                title=title,
                due_date=random.choice(due_dates),
                submitted=random.choice([True, False]),
                student=enrollment.student,
                course=enrollment.course
            )
        )

# ---------------------------
# Commit All
# ---------------------------
session.add_all(students + courses + enrollments + assignments)
session.commit()

print("✅ Seeded 1 teacher, 15 students, 5 courses, enrollments, and assignments.")
