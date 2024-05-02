from application.models import *
from application.resources import api
from application.security import user_datastore
from config import DevelopmentConfig
from flask import Flask
from flask_cors import CORS
from flask_security import Security
from application.worker import celery_init_app
from application.instances import cache
from celery.schedules import crontab
from application.tasks import daily_reminder, creator_report


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    cache.init_app(app)
    # celery_app = celery_init_app(app)
    # CORS(app, origins="http://localhost:8080", supports_credentials=True)
    app.security = Security(app, user_datastore)
    with app.app_context():
        import application.views
    return app


app = create_app()
CORS(app)
celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=21, minute=18),
        daily_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(hour=12, minute=6),
        creator_report.s(),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
