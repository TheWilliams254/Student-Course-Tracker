from app.models import Base, engine, Teacher
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Adding teachers
def default_teachers():
    if session.query(Teacher).count() == 0:
        t1 = Teacher(name="Albert", email="Albert@example.com")
        t1.set_password("Albert@Byrone;")
        session.add(t1)
        session.commit()
        print("✅ Added default teacher.")

if __name__ == "__main__":
    default_teachers()
