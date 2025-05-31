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


---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/TheWilliams254/student-course-tracker.git
cd student-course-tracker

2. **Create and activate a virtual environment:**
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Set environment variables (optional):

Create a .env file and add:
FLASK_APP=app.py
FLASK_ENV=development

5. Initialize the database:
    flask db upgrade
python app/seed.py   # (Optional) Seed initial data

6. Run the application:

 flask run

App will be available at http://localhost:5000
