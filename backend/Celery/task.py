from celery import shared_task
import time
from models import QuizAttempt, Quiz, Chapter, Subject , User
from datetime import datetime, timedelta, date
from flask import current_app
from flask_mail import Message
import flask_excel as excel
import os



@shared_task(ignore_result=False)
def export_user_quiz_history(user_id):
    """Export quiz history for a specific user using Flask-Excel."""
    try:
        # Get user attempts with related data
        attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
        
        if not attempts:
            return "NO_ATTEMPTS"  # Simple string instead of dictionary
        
        column_names = [column.name for column in QuizAttempt.__table__.columns]
        
        # Create directory if it doesn't exist
        os.makedirs('user-downloads', exist_ok=True)
        
        csv_out = excel.make_response_from_query_sets(attempts, column_names=column_names, file_type='csv')
        
        filename = f'{user_id}_quiz_history.csv'
        file_path = f'./user-downloads/{filename}'
        
        with open(file_path, 'wb') as file:
            file.write(csv_out.data)
        
        return filename
        
    except Exception as e:
        return "ERROR"  # Simple string instead of dictionary



@shared_task(ignore_result=False)
def send_daily_reminder():
    """Send daily quiz reminders to all active users."""
    try:
        # Get all active users
        users = User.query.filter_by(is_active=True).all()
        
        if not users:
            return "NO_USERS"
        
        # Get mail instance from current app
        mail = current_app.extensions.get('mail')
        if not mail:
            return "MAIL_NOT_CONFIGURED"
        
        sent_count = 0
        
        for user in users:
            try:
                # Simple greeting message
                msg = Message(
                    subject="Daily Quiz Reminder - Time to Test Your Knowledge!",
                    recipients=[user.email],
                    body=f"""
Hello {user.username},

Good day! 🌟

This is your daily reminder to check out the available quizzes and test your knowledge. 

Taking quizzes regularly helps you:
• Learn new concepts
• Test your understanding  
• Track your progress
• Stay engaged with your studies

Log in to your account and see what quizzes are waiting for you today!

Best regards,
Quiz Management Team
                    """
                )
                
                mail.send(msg)
                sent_count += 1
                
            except Exception as e:
                print(f"Failed to send reminder to {user.email}: {str(e)}")
                continue
        
        return f"SENT_TO_{sent_count}_USERS"
        
    except Exception as e:
        return "ERROR"


@shared_task(ignore_result=False)
def generate_monthly_report():
    """Generate monthly performance reports for all users."""
    try:
        # Get all active users
        users = User.query.filter_by(is_active=True).all()
        
        if not users:
            return "NO_USERS"
        
        # Calculate last month's date range
        today = date.today()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        # Get mail instance
        mail = current_app.extensions.get('mail')
        if not mail:
            return "MAIL_NOT_CONFIGURED"
        
        sent_count = 0
        
        for user in users:
            try:
                # Get user's attempts from last month
                attempts = QuizAttempt.query.filter(
                    QuizAttempt.user_id == user.id,
                    QuizAttempt.start_time >= datetime.combine(first_day_last_month, datetime.min.time()),
                    QuizAttempt.start_time <= datetime.combine(last_day_last_month, datetime.max.time()),
                    QuizAttempt.is_completed == True
                ).all()
                
                if not attempts:
                    # Send "no activity" report
                    msg = Message(
                        subject=f"Monthly Report - {last_day_last_month.strftime('%B %Y')}",
                        recipients=[user.email],
                        body=f"""
Hello {user.username},

Your Monthly Quiz Report for {last_day_last_month.strftime('%B %Y')}:

No quiz attempts were made this month.
We encourage you to participate more actively in upcoming quizzes!

Best regards,
Quiz Management Team
                        """
                    )
                else:
                    # Calculate statistics
                    total_quizzes = len(attempts)
                    total_score = sum(attempt.score for attempt in attempts)
                    
                    # Get quiz details for percentage calculation
                    quiz_scores = []
                    subject_performance = {}
                    
                    for attempt in attempts:
                        quiz = Quiz.query.get(attempt.quiz_id)
                        if quiz and quiz.total_marks > 0:
                            percentage = (attempt.score / quiz.total_marks) * 100
                            quiz_scores.append(percentage)
                            
                            # Track subject performance
                            chapter = Chapter.query.get(quiz.chapter_id)
                            if chapter:
                                subject = Subject.query.get(chapter.subject_id)
                                if subject:
                                    if subject.name not in subject_performance:
                                        subject_performance[subject.name] = []
                                    subject_performance[subject.name].append(percentage)
                    
                    avg_percentage = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
                    passed_quizzes = len([score for score in quiz_scores if score >= 60])  # Assuming 60% is pass
                    
                    # Create subject performance summary
                    subject_summary = []
                    for subject_name, scores in subject_performance.items():
                        avg_subject_score = sum(scores) / len(scores)
                        subject_summary.append(f"• {subject_name}: {avg_subject_score:.1f}% ({len(scores)} quizzes)")
                    
                    subject_details = "\n".join(subject_summary) if subject_summary else "No subject data available"
                    
                    msg = Message(
                        subject=f"Monthly Report - {last_day_last_month.strftime('%B %Y')}",
                        recipients=[user.email],
                        body=f"""
Hello {user.username},

Your Monthly Quiz Report for {last_day_last_month.strftime('%B %Y')}:

📊 Overall Performance:
• Quizzes Attempted: {total_quizzes}
• Average Score: {avg_percentage:.1f}%
• Quizzes Passed: {passed_quizzes}/{total_quizzes}
• Total Points Earned: {total_score}

📚 Subject-wise Performance:
{subject_details}

{"🎉 Great job this month!" if avg_percentage >= 80 else "💪 Keep up the good work!" if avg_percentage >= 60 else "📈 There's room for improvement - you can do it!"}

Best regards,
Quiz Management Team
                        """
                    )
                
                mail.send(msg)
                sent_count += 1
                
            except Exception as e:
                print(f"Failed to send monthly report to {user.email}: {str(e)}")
                continue
        
        return f"REPORTS_SENT_TO_{sent_count}_USERS"
        
    except Exception as e:
        return "ERROR"
