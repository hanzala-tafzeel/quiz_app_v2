from celery import Celery, Task
from flask import Flask
from celery.schedules import crontab

class CeleryConfig:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'
    timezone = 'Asia/Kolkata'

        # Add beat schedule for periodic tasks
    beat_schedule = {
        'daily-reminder': {
            'task': 'Celery.tasks.send_daily_reminder',  # Adjust path based on your structure
            'schedule': crontab(hour=15, minute=58),  # Every day at 9:00 AM
        },
        'monthly-report': {
            'task': 'Celery.tasks.generate_monthly_report',  # Adjust path based on your structure
            'schedule': crontab(day_of_month=26, hour=16, minute=3),  # 1st day of month at 10:00 AM
        },
    }



def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app