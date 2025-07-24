# Quiz Master - V1


## Installation and Setup
### Prerequisites:
- Python 
- Git (for cloning the repository)
- Virtual environment setup

### Steps to Run the Application:
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd quiz_app
   ```
2. **Create a Virtual Environment and Activate It:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```
3. **Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access the App in Browser:**
   ```
http://127.0.0.1:5000
```


## Overview
Quiz Master is a multi-user web application designed for exam preparation across multiple courses. The platform supports two roles: an administrator (Quiz Master) and users (students). The administrator manages subjects, chapters, quizzes, and questions, while users can register, log in, and attempt quizzes on their chosen subjects.

## Features
### Admin Features:
- Superuser with full control over the platform.
- Can create, edit, and delete subjects and chapters.
- Can create and manage quizzes under specific chapters.
- Can add multiple-choice questions (MCQs) to quizzes.
- Can view and manage users.
- Can view quiz scores and generate summary charts.

### User Features:
- User registration and login.
- Can select subjects and chapters to attempt quizzes.
- Each quiz has a time duration (optional timer feature).
- Scores are recorded for each quiz attempt.
- Can view past quiz scores and performance analytics.

## Tech Stack
- **Backend:** Flask (Python), Flask-Login, Flask-SQLAlchemy
- **Frontend:** Jinja2, HTML, CSS, Bootstrap
- **Database:** SQLite (mandatory)
- **APIs:** Flask-Restful (for API endpoints, optional)
- **Charts & Visualizations:** Chart.js (optional)



