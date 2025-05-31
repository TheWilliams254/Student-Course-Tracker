# 🎓 Student Course Tracker

The **Student Course Tracker** is a Flask-based web application that allows students and teachers to manage courses, assignments, and progress tracking. It supports assignment submission, approval, PDF/CSV export, and role-based dashboards.

---

## 🚀 Features

### 🧑‍🎓 Students
- Secure login
- View enrolled courses
- Submit assignments
- Track assignment approval status

### 👩‍🏫 Teachers
- Login and access personalized dashboard
- View all students and their courses
- Approve or reject submitted assignments
- Export assignment data as CSV or PDF

---

## 🛠 Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, Bootstrap, Jinja2 Templates
- **Database**: SQLite
- **Authentication**: Flask-Login
- **PDF Generation**: ReportLab
- **CSV Export**: Python CSV module
- **ORM Migration**: Alembic

---

## 📁 Project Structure
student-course-tracker/
├── app/
│ ├── init.py # Flask app factory
│ ├── models.py # SQLAlchemy models
│ ├── pdf_utils.py # PDF export functionality
│ ├── seed.py # Script to populate initial data
│ ├── student-tracker.db # SQLite database file
│ ├── migrations/ # Alembic migration scripts
│ └── pycache/ # Compiled Python cache
│
├── static/ # Static assets (CSS, JS, images)
├── templates/ # HTML templates using Jinja2
│
├── app.py # Main Flask runner (can be renamed run.py)
├── main.py # Optional: handles route logic or main entry
├── alembic.ini # Alembic configuration file
├── .gitignore # Files and folders to ignore in Git
├── Pipfile # Pipenv dependency manager
├── Pipfile.lock # Pipenv lock file
├── Procfile # Deployment configuration (e.g., Heroku)
├── requirements.txt # Python dependencies (pip install -r)
├── README.md # Project documentation
└── student-tracker.db # Duplicate DB (optional - move to app/)

