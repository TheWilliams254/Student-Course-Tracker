# models.py

#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///student-tracker.db')

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    gpa = Column(Float)

    enrollments = relationship("Enrollment", back_populates="student")
    assignments = relationship("Assignment", back_populates="student")

    def __repr__(self):
        return f"Student(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, gpa={self.gpa})"
    
class Course(Base):
     __tablename__ = 'courses'
     id = Column(Integer, primary_key=True)
     name = Column(String(50))
     code = Column(String(50))
     semester = Column(String(50))

     enrollments = relationship("Enrollment", back_populates="course")
     assignments = relationship("Assignment", back_populates="course")

     def __repr__(self):
            return f"Course(id={self.id}, title={self.title}, code={self.code})"

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"Enrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id})"

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    title =  Column(String(50))
    due_date = Column(DateTime)
    submitted = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    student = relationship("Student", back_populates="assignments")
    course = relationship("Course", back_populates="assignments")

    def __repr__(self):
        return f"Assignment(id={self.id}, student_id={self.student_id}, course_id={self.course_id})"