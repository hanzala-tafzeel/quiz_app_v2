# quiz_app_v2
A modern quiz application built with Vue.js for the frontend and Python for the backend. This project is designed to provide an interactive quiz experience with a clean and responsive user interface.

## Features
- User-friendly quiz interface  
- Dynamic questions and answers  
- Score calculation and summary  
- Responsive design for desktop and mobile  
- Background task processing with Celery
- Redis caching for improved performance
- Scheduled tasks and email notifications
- Easily extendable and customizable

## Tech Stack
- **Frontend:** Vue.js, JavaScript, HTML, CSS  
- **Backend:** Python Flask
- **Caching & Message Broker:** Redis
- **Background Tasks:** Celery Worker
- **Task Scheduler:** Celery Beat
- **Email:** Flask-Mail

## Getting Started
### Prerequisites
- Node.js & npm  
- Python 3.x
- Redis server

### Installation
#### Clone the repository
```bash
git clone https://github.com/hanzala-tafzeel/quiz_app_v2.git
cd quiz_app_v2
```

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Start Redis Server
```bash
# On macOS (using Homebrew)
brew services start redis

# On Ubuntu/Debian
sudo systemctl start redis-server

# On Windows (if installed via MSI)
redis-server
```

#### Start Celery Worker
```bash
cd backend
celery -A app.celery worker --loglevel=info
```

#### Start Celery Beat (for scheduled tasks)
```bash
cd backend
celery -A app.celery beat --loglevel=info
```

#### Run Backend Server
```bash
cd backend
python app.py
```

#### Frontend Setup
```bash
cd quizmaster
npm install
npm run serve
```

## Usage
1. Start Redis server
2. Start Celery worker (for background tasks)
3. Start Celery Beat (for scheduled tasks)
4. Start the backend server
5. Run the frontend development server
6. Visit `http://localhost:8080` (or the specified port) in your browser
7. Enjoy taking quizzes!

## Folder Structure
```
quiz_app_v2/
├── quizmaster/      # Vue.js application
├── backend/         # Python backend
├── README.md
└── ...
```

## Background Tasks
The application uses Celery for handling background tasks such as:
- Email notifications
- Quiz result processing
- Scheduled maintenance tasks
- Cache management

## Acknowledgements
- Vue.js Documentation  
- Python Documentation
- Redis Documentation
- Celery Documentation
