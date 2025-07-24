# app.py - Refactored Flask Application
from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_jwt_extended import JWTManager 


app = None  # Placeholder for the Flask app instance

def create_app():
    """Application factory pattern for better organization"""
    quiz_app = Flask(__name__)
    
    # Configuration
    quiz_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.sqlite3"
    quiz_app.config['SECRET_KEY'] = "QuizApp"
    quiz_app.config["JWT_SECRET_KEY"] = "super-secret-key"
    quiz_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    jwt = JWTManager(quiz_app)
    db.init_app(quiz_app)
    # added jwt for token based authentication
    jwt.init_app(quiz_app)
    
    # Configure CORS
    CORS(quiz_app,
         origins=["http://localhost:8080", "http://192.168.1.8:8080"],
         allow_headers=["Content-Type", "Authorization", "Cookie"],
         supports_credentials=True)
    
    # Set debug mode
    quiz_app.debug = True
    
    # Create application context
    with quiz_app.app_context():
        db.create_all()
        
        # Ensure admin user exists
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

if __name__ == "__main__":
    app.run(debug=True)