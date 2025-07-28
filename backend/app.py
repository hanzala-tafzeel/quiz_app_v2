from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_caching import Cache
from Celery.celery_factory import celery_init_app
import flask_excel as excel
from flask_mail import Mail



app = None  # Placeholder for the Flask app instance
migrate = None


def create_app():
    """Application factory pattern for better organization"""
    quiz_app = Flask(__name__)
    
    # Configuration
    quiz_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.sqlite3"
    quiz_app.config['SECRET_KEY'] = "QuizApp"
    quiz_app.config["JWT_SECRET_KEY"] = "super-secret-key"
    quiz_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    quiz_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    quiz_app.config["CACHE_TYPE"] = "RedisCache"
    quiz_app.config["CACHE_REDIS_PORT"] = 6379
    quiz_app.config["CACHE_DEFAULT_TIMEOUT"] = 30

    #flask mail configuration
    quiz_app.config["MAIL_SERVER"] = "smtp.gmail.com"
    quiz_app.config["MAIL_PORT"] = 587
    quiz_app.config["MAIL_USE_TLS"] = True
    quiz_app.config["MAIL_USERNAME"] = "hanzalatafzeel44@gmail.com"
    quiz_app.config["MAIL_PASSWORD"] = "qlfrhjwdoxqpytei"  
    quiz_app.config["MAIL_DEFAULT_SENDER"] = "hanzalatafzeel44@gmail.com"



    
    # Initialize extensions
    jwt = JWTManager(quiz_app)
    db.init_app(quiz_app)

    cache = Cache(quiz_app)
    jwt.init_app(quiz_app)

    # Initialize Flask-Mail
    mail = Mail(quiz_app)
    quiz_app.mail = mail  # Make mail accessible through app instance

    #initialize migration
    migrate = Migrate(quiz_app, db)

    quiz_app.cache = cache
    
    # Configure CORS
    CORS(quiz_app,
         origins=["http://localhost:8080", "http://192.168.1.8:8080"],
         allow_headers=["Content-Type", "Authorization", "Cookie"],
         supports_credentials=True)
    
    # Set debug mode
    quiz_app.debug = True
    
    # Create application context
    with quiz_app.app_context():
        
        # Ensure admin user exists

        try:
            if not User.query.filter_by(role="admin").first():
                admin_user = User(
                    username="admin",
                    email="admin@gmail.com",
                    password=generate_password_hash("admin123"),
                    role="admin"
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created with email 'admin@gmail.com' and password 'admin123'.")
        except Exception as e:
            # Handle case when tables don't exist yet
            print(f"Note: Could not create admin user. Run migrations first. Error: {e}")
    
    print("Quiz App Initialized")
    return quiz_app

def init_app():
    """Initialize the Flask application"""
    global app
    app = create_app()
    
    # Import routes after app creation to avoid circular imports
    from controllers.controller import register_routes
    register_routes(app)
    
    return app

# Initialize the app
app = init_app()

# Initialize Celery
celery_app = celery_init_app(app)

# Initialize Flask-Excel
excel.init_excel(app)

if __name__ == "__main__":
    app.run(debug=True)