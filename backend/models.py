from datetime import datetime
from flask_login import UserMixin 
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # instance of sqlalchemy is created


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, default="user")
    phone = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "is_active": self.is_active
        }


class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    chapters = db.relationship('Chapter', cascade='all,delete', backref='subject', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "is_active": self.is_active,
            "chapters": [c.to_dict() for c in self.chapters],
            "chapters_count": len(self.chapters) if self.chapters else 0
        }


class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    # relationship between chapter and quiz
    quizzes = db.relationship('Quiz', cascade='all,delete', backref='chapter', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject_id": self.subject_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "is_active": self.is_active,
            "quizzes_count": len(self.quizzes) if self.quizzes else 0
        }


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    schedule_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    total_marks = db.Column(db.Integer, default=0)
    pass_marks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    # relationship with quizattempt and question
    questions = db.relationship('Question', cascade='all,delete', backref='quiz', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "schedule_date": self.schedule_date.strftime("%Y-%m-%d %H:%M:%S") if self.schedule_date else None,
            "duration": self.duration,
            "chapter_id": self.chapter_id,
            "total_marks": self.total_marks,
            "pass_marks": self.pass_marks,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "is_active": self.is_active,
            "questions" : [q.to_dict() for q in self.questions],
            "questions_count": len(self.questions) if self.questions else 0
        }


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_text = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_opt = db.Column(db.Integer, nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # relationship with questionresponse and question
    responses = db.relationship('QuestionResponse', cascade='all,delete', backref='question', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "question_text": self.question_text,
            "option1": self.option1,
            "option2": self.option2,
            "option3": self.option3,
            "option4": self.option4,
            "correct_opt": self.correct_opt,
            "marks": self.marks,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


class QuizAttempt(db.Model):
    __tablename__ = "quizattempt"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    strat_time = db.Column(db.DateTime, default=datetime.now())
    end_time = db.Column(db.DateTime, default=datetime.now())
    is_completed = db.Column(db.Boolean, default=True)
    score = db.Column(db.Integer, default=0)

    user = db.relationship('User', cascade='all,delete', backref='quizattempt', lazy=True)
    quiz = db.relationship('Quiz', cascade='all,delete', backref='quizattempt', lazy=True)
    responses = db.relationship('QuestionResponse', cascade='all,delete', backref='quizattempt', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "strat_time": self.strat_time.strftime("%Y-%m-%d %H:%M:%S") if self.strat_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            "is_completed": self.is_completed,
            "score": self.score,
            "responses_count": len(self.responses) if self.responses else 0
        }


class QuestionResponse(db.Model):
    __tablename__ = "questionresponse"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    attempt_id = db.Column(db.Integer, db.ForeignKey("quizattempt.id"), nullable=False)
    selected_option = db.Column(db.Integer, nullable=True)
    is_correct = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "attempt_id": self.attempt_id,
            "selected_option": self.selected_option,
            "is_correct": self.is_correct
        }