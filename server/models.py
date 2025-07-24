# models.py

#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship,sessionmaker
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    registration_number = Column(String, unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    gpa = Column(Float)

    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.registration_number} - {self.first_name} {self.last_name}>"
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(64), nullable=False)   

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        if not self.password_hash:
            return False
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    def __repr__(self):
        return f"Teacher(id={self.id}, name={self.name}, email={self.email})"
class Course(Base):
     __tablename__ = 'courses'
     id = Column(Integer, primary_key=True)
     name = Column(String(50))
     code = Column(String(50))
     credits = Column(Integer)
     semester = Column(String(50))

     enrollments = relationship("Enrollment", back_populates="course")
     assignments = relationship("Assignment", back_populates="course")

     def __repr__(self):
            return f"Course(id={self.id}, name={self.name}, code={self.code}),credits={self.credits}, semester={self.semester})"

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
    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
