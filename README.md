🎓 Student Course Tracker
The Student Course Tracker is a web-based application built with Flask that allows students and teachers to manage courses, assignments, and progress in a structured and efficient manner.

🚀 Features
🧑‍🎓 Students
Register and log in securely

View enrolled courses

Submit assignments

Track assignment status (Pending/Approved)

👩‍🏫 Teachers
Log in and access a dashboard

View all students and their enrolled courses

Approve/reject assignment submissions

Export assignment submissions to CSV or PDF

Manage assignments and courses

📊 Admin Dashboard (optional)
Overview of total students, courses, and assignments

Graphs and statistics (optional)

Responsive design with sidebar navigation

🛠️ Technologies Used
Backend: Python, Flask, SQLAlchemy ORM

Frontend: HTML, CSS, Bootstrap, Jinja2 Templates

Database: SQLite (can be swapped for PostgreSQL)

Authentication: Flask-Login

PDF/CSV Export: ReportLab, CSV module

📦 Installation & Setup
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/TheWilliams254/student-course-tracker.git
cd student-course-tracker
2. Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Initialize the database
bash
Copy
Edit
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
5. Run the server
bash
Copy
Edit
flask run

The app will be available at http://localhost:5000.
student-course-tracker/
├── app/
│   ├── __pycache__/                  # Python bytecode cache (auto-generated)
│   ├── migrations/                   # Alembic migration files for the database
│   ├── __init__.py                   # Initializes the Flask app
│   ├── models.py                     # SQLAlchemy database models
│   ├── pdf_utils.py                  # Utilities for generating PDFs
│   ├── seed.py                       # Optional script to seed the database
│   └── student-tracker.db            # SQLite database file
│
├── static/                           # Static files (CSS, JS, images)
├── templates/                        # HTML templates (Jinja2)
│
├── app.py                            # Main Flask app runner (can be renamed to run.py)
├── main.py                           # Possibly contains route logic or entry point
├── alembic.ini                       # Alembic configuration file
├── .gitignore                        # Git ignore rules
├── Pipfile                           # Pipenv environment dependencies
├── Pipfile.lock                      # Lock file for pipenv
├── Procfile                          # For deployment (e.g., on Heroku)
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
└── student-tracker.db                # (Duplicate?) Consider storing DB only in `/app`

Students sign up and log in to view their dashboard.

Teachers log in to view and manage assignment submissions.

The teacher dashboard provides a sidebar menu for quick navigation.

Assignments can be filtered, paginated, and exported.

🌐 Deployment
You can deploy this app using:

Render

Replit

Fly.io

Or any WSGI-compatible hosting service

📌 Future Improvements
Role-based admin control panel

Email notifications

Search/filter by course or assignment

Analytics and reporting dashboard

REST API integration for mobile clients

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is licensed under the MIT License.

