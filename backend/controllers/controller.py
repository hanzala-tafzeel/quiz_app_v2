# routes.py - Standard Flask Routes (converted from Flask-RESTful)
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps

from models import db, User, Subject, Chapter, Quiz, Question, QuizAttempt, QuestionResponse

# ------------------------------ Auth Helpers ----------------------------- #

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper

# ------------------------------ Utility ----------------------------- #

def register_routes(app):
    """Register all routes with the Flask app"""

    # ------------------------------ User Routes ----------------------------- #

    @app.route('/api/users', methods=['GET'])
    @jwt_required()
    @admin_required
    def list_users():
        users = User.query.all()
        return jsonify({"users": [u.to_dict() for u in users]})

    @app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
    @admin_required
    def user_detail(user_id):
        user = User.query.get_or_404(user_id)
        if request.method == 'GET':
            return jsonify(user.to_dict())
        elif request.method == 'PUT':
            data = request.get_json() or {}
            user.username = data.get('username', user.username)
            user.phone = data.get('phone', user.phone)
            user.is_active = data.get('is_active', user.is_active)
            db.session.commit()
            return jsonify({"message": "User updated successfully", "user": user.to_dict()})
        else:  # DELETE
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})

    @app.route('/api/users/search', methods=['POST'])
    @jwt_required()
    @admin_required
    def user_search():
        data = request.get_json() or {}
        search_text = (data.get('search') or '').strip().lower()
        search_by = (data.get('search_by') or 'username').strip().lower()
        if search_by == 'username':
            users = User.query.filter(User.username.ilike(f"%{search_text}%")).all()
        elif search_by == 'email':
            users = User.query.filter(User.email.ilike(f"%{search_text}%")).all()
        else:
            users = User.query.filter(User.phone.ilike(f"%{search_text}%")).all()
        return jsonify({"users": [u.to_dict() for u in users]})

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = (data.get('email') or '').lower()
        password = data.get('password') or ''
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Email not registered"}), 401
        if not user.is_active:
            return jsonify({"error": "User is inactive"}), 403
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Wrong password"}), 401
        token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Login successful", "token": token, "user": user.to_dict(), "role": user.role})

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        username = data.get('fullname')
        email = (data.get('email') or '').lower()
        password = data.get('password')
        phone = data.get('mobile')
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists"}), 409
        new_user = User(username=username, password=generate_password_hash(password), email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful", "user_id": new_user.id})


    @app.route('/api/user', methods=['GET', 'PUT'])
    @jwt_required()
    def current_user():
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        if request.method == 'GET':
            return jsonify(user.to_dict())
        
        data = request.get_json() or {}
        user.username = data.get('username', user.username)
        user.phone = data.get('phone', user.phone)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully", "user": user.to_dict()})

    # ------------------------------ Subject Routes ----------------------------- #

    @app.route('/api/subjects', methods=['GET', 'POST'])
    def subjects():
        if request.method == 'GET':
            subjects = Subject.query.all()
            return jsonify({"subjects": [s.to_dict() for s in subjects]})
        verify_jwt_in_request()
        admin_required(lambda: None)()
        data = request.get_json() or {}
        name = data.get('name')
        if Subject.query.filter_by(name=name).first():
            return jsonify({"error": "Subject already exists"}), 409
        new_subject = Subject(name=name, description=data.get('description'))
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({"message": "Subject added successfully"})

    @app.route('/api/subjects/<int:subject_id>', methods=['GET', 'PUT', 'DELETE'])
    def subject_detail(subject_id):
        subject = Subject.query.get_or_404(subject_id)
        if request.method == 'GET':
            return jsonify(subject.to_dict())
        verify_jwt_in_request()
        admin_required(lambda: None)()
        if request.method == 'PUT':
            data = request.get_json() or {}
            subject.name = data.get('subject', subject.name)
            subject.description = data.get('description', subject.description)
            db.session.commit()
            return jsonify({"message": "Subject updated successfully", "subject": subject.to_dict()})
        db.session.delete(subject)
        db.session.commit()
        return jsonify({"message": "Subject deleted successfully"})

    @app.route('/api/subjects/search', methods=['POST'])
    def subject_search():
        data = request.get_json() or {}
        search_text = (data.get('search') or '').strip().lower()
        subjects = Subject.query.filter(Subject.name.ilike(f"%{search_text}%")).all()
        return jsonify({"subjects": [s.to_dict() for s in subjects]})

    # ------------------------------ Chapter Routes ----------------------------- #

    @app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET', 'POST'])
    def chapter_list(subject_id):
        if request.method == 'GET':
            chapters = Chapter.query.filter_by(subject_id=subject_id).all()
            return jsonify({"chapters": [c.to_dict() for c in chapters]})
        
        verify_jwt_in_request()
        admin_required(lambda: None)()
        data = request.get_json()
        name = data.get('name')
        description =data.get('description')
        if Chapter.query.filter_by(name=name).first():
            return jsonify({"error": "Chapter already exists"}), 409
        new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return jsonify({"message": "Chapter added successfully", "chapter": new_chapter.to_dict()})
    
    @app.route('/api/chapters', methods = ['GET'])
    def chapters():
        chapters = Chapter.query.all()
        return jsonify({"chapters": [c.to_dict() for c in chapters]})
    

    @app.route('/api/chapters/<int:chapter_id>', methods=['GET', 'PUT', 'DELETE'])
    def chapter_detail(chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        if request.method == 'GET':
            return jsonify(chapter.to_dict())
        verify_jwt_in_request()
        admin_required(lambda: None)()
        if request.method == 'PUT':
            data = request.get_json() or {}
            chapter.name = data.get('chapter', chapter.name)
            chapter.description = data.get('description', chapter.description)
            db.session.commit()
            return jsonify({"message": "Chapter updated successfully", "chapter": chapter.to_dict()})
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({"message": "Chapter deleted successfully"})

    # ------------------------------ Quiz Routes ----------------------------- #

    @app.route('/api/quizzes', methods=['GET', 'POST'])
    def quizzes():
        if request.method == 'GET':
            quizzes = Quiz.query.all()
            return jsonify({"quizzes": [q.to_dict() for q in quizzes]})
        verify_jwt_in_request()
        admin_required(lambda: None)()
        data = request.get_json() or {}
        new_quiz = Quiz(
            title=data.get('title'),
            description=data.get('description'),
            duration=data.get('duration'),
            schedule_date=datetime.strptime(data.get('date'), "%Y-%m-%d").date(),
            chapter_id=data.get('chapter_id')
        )
        db.session.add(new_quiz)
        db.session.commit()
        return jsonify({"message": "Quiz added successfully", "quizzes": new_quiz.to_dict()})


    @app.route('/api/quizzes/<int:quiz_id>', methods=['GET', 'PUT', 'DELETE'])
    def quiz_detail(quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        if request.method == 'GET':
            return jsonify(quiz.to_dict())
        verify_jwt_in_request()
        admin_required(lambda: None)()
        if request.method == 'PUT':
            data = request.get_json() or {}
            quiz.title = data.get('title', quiz.title)
            quiz.description = data.get('description', quiz.description)
            quiz.duration = data.get('duration', quiz.duration)
            if data.get('date'):
                quiz.schedule_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
            quiz.is_active = data.get('is_active', quiz.is_active)
            db.session.commit()
            return jsonify({"message": "Quiz updated successfully", "quiz": quiz.to_dict()})
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({"message": "Quiz deleted successfully"})

    @app.route('/api/quizzes/search', methods=['POST'])
    def quiz_search():
        data = request.get_json() or {}
        search_text = (data.get('search') or '').strip().lower()
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{search_text}%")).all()
        return jsonify({"quizzes": [q.to_dict() for q in quizzes]})

    @app.route('/api/quizzes/active', methods=['GET'])
    @jwt_required()
    def active_quizzes():
        active_quizzes = Quiz.query.filter_by(is_active=True).all()
        current_date = date.today()
        quizzes_data = []
        for quiz in active_quizzes:
            qd = quiz.to_dict()
            qd['is_available'] = quiz.schedule_date <= current_date
            quizzes_data.append(qd)
        return jsonify({"quizzes": quizzes_data})

    # ------------------------------ Question Routes ----------------------------- #

    @app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET', 'POST'])
    def question_list(quiz_id):
        if request.method == 'GET':
            questions = Question.query.filter_by(quiz_id=quiz_id).all()
            return jsonify({"questions": [q.to_dict() for q in questions]})
        verify_jwt_in_request()
        admin_required(lambda: None)()
        data = request.get_json() or {}
        new_question = Question(
            quiz_id=quiz_id,
            question_text=data.get('question_text'),
            option1=data.get('option1'),
            option2=data.get('option2'),
            option3=data.get('option3'),
            option4=data.get('option4'),
            correct_opt=data.get('correct_opt'),
            marks=data.get('marks')
        )
        # Update quiz marks
        quiz = Quiz.query.get_or_404(quiz_id)
        quiz.total_marks += int(new_question.marks)
        quiz.pass_marks = 0.55 * quiz.total_marks
        db.session.add(new_question)
        db.session.commit()
        return jsonify({"message": "Question added successfully", "question": new_question.to_dict()})

    @app.route('/api/questions/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
    def question_detail(question_id):
        question = Question.query.get_or_404(question_id)
        if request.method == 'GET':
            return jsonify(question.to_dict())
        verify_jwt_in_request()
        admin_required(lambda: None)()
        original_marks = question.marks
        if request.method == 'PUT':
            data = request.get_json() or {}
            question.question_text = data.get('question', question.question_text)
            question.option1 = data.get('option1', question.option1)
            question.option2 = data.get('option2', question.option2)
            question.option3 = data.get('option3', question.option3)
            question.option4 = data.get('option4', question.option4)
            question.correct_opt = data.get('correctOption', question.correct_opt)
            question.marks = data.get('marks', question.marks)
            # Update quiz marks
            quiz = Quiz.query.get(question.quiz_id)
            marks_diff = int(original_marks) - int(question.marks)
            quiz.total_marks -= marks_diff
            quiz.pass_marks = 0.55 * quiz.total_marks
            db.session.commit()
            return jsonify({"message": "Question updated successfully", "question": question.to_dict()})
        # DELETE
        quiz = Quiz.query.get(question.quiz_id)
        quiz.total_marks -= question.marks
        quiz.pass_marks = 0.55 * quiz.total_marks
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Question deleted successfully"})

    # ------------------------------ Quiz Attempt Routes ----------------------------- #

    @app.route('/api/attempts', methods=['GET'])
    @jwt_required()
    def attempts_list():
        user_id = get_jwt_identity()
        attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
        attempts_list = []
        for attempt in attempts:
            quiz = Quiz.query.get(attempt.quiz_id)
            attempts_list.append({
                "id": attempt.id,
                "quiz_id": attempt.quiz_id,
                "start_time": attempt.strat_time.isoformat() if attempt.strat_time else None,
                "end_time": attempt.end_time.isoformat() if attempt.end_time else None,
                "is_completed": attempt.is_completed,
                "score": attempt.score,
                "total_marks": quiz.total_marks if quiz else 0,
                "quiz_title": quiz.title if quiz else '',
                "percentage": (attempt.score / quiz.total_marks * 100) if quiz and quiz.total_marks > 0 else 0
            })
        return jsonify({"attempts": attempts_list})

    @app.route('/api/quizzes/<int:quiz_id>/attempt', methods=['GET', 'POST'])
    @jwt_required()
    def attempt_quiz(quiz_id):
        quiz = Quiz.query.filter_by(id=quiz_id, is_active=True).first_or_404()
        if request.method == 'GET':
            return jsonify({
                "id": quiz.id,
                "title": quiz.title,
                "duration": quiz.duration * 60,
                "total_marks": quiz.total_marks,
                "questions": [{
                    "id": q.id,
                    "text": q.question_text,
                    "options": [q.option1, q.option2, q.option3, q.option4],
                    "marks": q.marks
                } for q in quiz.questions]
            })
        # POST
        data = request.get_json() or {}
        responses = data.get('responses', [])
        user_id = get_jwt_identity()
        quiz_attempt = QuizAttempt(user_id=user_id, quiz_id=quiz.id, strat_time=datetime.now(), is_completed=True)
        db.session.add(quiz_attempt)
        db.session.commit()
        score = 0
        saved_responses = []
        for r in responses:
            q_id = r.get('question_id')
            sel_opt = r.get('selected_option')
            question = Question.query.get_or_404(q_id)
            is_correct = (int(sel_opt) + 1 == question.correct_opt)
            if is_correct:
                score += question.marks
            qr = QuestionResponse(question_id=q_id, attempt_id=quiz_attempt.id, selected_option=sel_opt, is_correct=is_correct)
            db.session.add(qr)
            saved_responses.append({"question_id": q_id, "selected_option": sel_opt, "is_correct": is_correct})
        quiz_attempt.score = score
        quiz_attempt.end_time = datetime.now()
        db.session.commit()
        return jsonify({
            "attempt_id": quiz_attempt.id,
            "score": score,
            "total_marks": quiz.total_marks,
            "percentage": (score / quiz.total_marks * 100) if quiz.total_marks > 0 else 0,
            "passed": score >= quiz.pass_marks,
            "responses": saved_responses
        })

    @app.route('/api/attempts/<int:attempt_id>', methods=['GET'])
    @jwt_required()
    def attempt_detail(attempt_id):
        user_id = get_jwt_identity()
        attempt = QuizAttempt.query.filter_by(id=attempt_id, user_id=user_id).first_or_404()
        quiz = Quiz.query.get_or_404(attempt.quiz_id)
        responses = QuestionResponse.query.filter_by(attempt_id=attempt_id).all()
        return jsonify({
            "id": quiz.id,
            "title": quiz.title,
            "total_marks": quiz.total_marks,
            "score": attempt.score,
            "percentage": (attempt.score / quiz.total_marks * 100) if quiz.total_marks > 0 else 0,
            "passed": attempt.score >= quiz.pass_marks,
            "start_time": attempt.strat_time.isoformat() if attempt.strat_time else None,
            "end_time": attempt.end_time.isoformat() if attempt.end_time else None,
            "questions": [{
                "id": q.id,
                "text": q.question_text,
                "options": [q.option1, q.option2, q.option3, q.option4],
                "correct_option": q.correct_opt - 1,
                "marks": q.marks,
                "selected_option": next((r.selected_option for r in responses if r.question_id == q.id), None),
                "is_correct": next((r.is_correct for r in responses if r.question_id == q.id), None)
            } for q in quiz.questions]
        })

    # ------------------------------ Summary Routes ----------------------------- #

    @app.route('/api/summary', methods=['GET'])
    @jwt_required()
    def user_summary():
        user_id = get_jwt_identity()
        attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
        quizzes_taken = len(attempts)
        normalized_scores = [a.score / Quiz.query.get(a.quiz_id).total_marks * 100 for a in attempts if Quiz.query.get(a.quiz_id).total_marks > 0]
        avg_score = sum(normalized_scores) / quizzes_taken if quizzes_taken > 0 else 0
        passed = [a for a in attempts if a.score >= Quiz.query.get(a.quiz_id).pass_marks]
        pass_rate = len(passed) / quizzes_taken * 100 if quizzes_taken > 0 else 0
        upcoming_quizzes = Quiz.query.filter(Quiz.schedule_date > datetime.now(), Quiz.is_active == True).count()
        recent_attempts = QuizAttempt.query.filter(QuizAttempt.user_id == user_id).order_by(QuizAttempt.strat_time.desc()).limit(5).all()
        recent_attempts_data = [{
            'attempt_id': a.id,
            'quiz_id': a.quiz_id,
            'quiz_title': Quiz.query.get(a.quiz_id).title,
            'date': a.strat_time.strftime('%Y-%m-%d'),
            'score': round(a.score / Quiz.query.get(a.quiz_id).total_marks * 100, 1)
        } for a in recent_attempts]
        subject_perf = {}
        for a in attempts:
            quiz = Quiz.query.get(a.quiz_id)
            subject = Subject.query.get(Chapter.query.get(quiz.chapter_id).subject_id)
            key = subject.name
            subject_perf.setdefault(key, []).append(a.score / quiz.total_marks * 100)
        subject_analytics = [{"subject": k, "avg_score": sum(v)/len(v), "attempts": len(v)} for k, v in subject_perf.items()]
        return jsonify({
            "summary": {
                "quizzes_taken": quizzes_taken,
                "avg_score": round(avg_score, 1),
                "upcoming_quizzes": upcoming_quizzes,
                "pass_rate": round(pass_rate, 1)
            },
            "recent_attempts": recent_attempts_data,
            "subject_performance": subject_analytics
        })

    @app.route('/api/admin/summary', methods=['GET'])
    @jwt_required()
    @admin_required
    def admin_summary():
        total_users = User.query.count()
        active_quizzes = Quiz.query.filter_by(is_active=True).count()
        total_subjects = Subject.query.count()
        total_quizzes = Quiz.query.count()
        total_attempts = QuizAttempt.query.count()
        today = date.today()
        attempts_today = [a for a in QuizAttempt.query.all() if a.strat_time and a.strat_time.date() == today]
        attempts_today_data = []
        for a in attempts_today:
            user = User.query.get(a.user_id)
            quiz = Quiz.query.get(a.quiz_id)
            attempts_today_data.append({
                'user': user.username if user else 'Unknown',
                'quiz_title': quiz.title if quiz else 'Unknown',
                'score': a.score,
                'time': a.strat_time.strftime('%H:%M'),
                'completed': a.is_completed
            })
        subject_perf = {}
        for sub in Subject.query.all():
            subject_perf[sub.name] = {'total_score': 0, 'attempt_count': 0}
        for a in QuizAttempt.query.all():
            quiz = Quiz.query.get(a.quiz_id)
            chapter = Chapter.query.get(quiz.chapter_id)
            subject = Subject.query.get(chapter.subject_id)
            subject_perf[subject.name]['total_score'] += a.score
            subject_perf[subject.name]['attempt_count'] += 1
        subject_analytics = [{
            "subject": s,
            "avg_score": (d['total_score']/d['attempt_count']*10) if d['attempt_count']>0 else 0,
            "attempts": d['attempt_count']
        } for s, d in subject_perf.items()]
        subject_attempt_distribution = [{"subject": s, "count": d['attempt_count']} for s, d in subject_perf.items()]
        # Top performers
        top_performers = []
        for q in Quiz.query.all():
            attempts = QuizAttempt.query.filter_by(quiz_id=q.id).order_by(QuizAttempt.score.desc()).limit(3).all()
            performers = [{"username": User.query.get(a.user_id).username, "score": a.score} for a in attempts if User.query.get(a.user_id)]
            if performers:
                top_performers.append({"quiz_title": q.title, "performers": performers})
        return jsonify({
            "stats": {
                "total_users": total_users,
                "total_quizzes": total_quizzes,
                "active_quizzes": active_quizzes,
                "total_subjects": total_subjects,
                "total_attempts": total_attempts
            },
            "attempts_today": attempts_today_data,
            "subject_performance": subject_analytics,
            "attempt_distribution": subject_attempt_distribution,
            "top_performers": top_performers
        })
