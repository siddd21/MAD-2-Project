from celery import shared_task
from .models import *
from .mail_service import send_message
from datetime import datetime, timedelta
from jinja2 import Template
import os

base_dir = "/home/sidd/STUDY/MAD-2/Project/backend/templates"
creator_report_path = os.path.join(base_dir, "creator_report.html")


@shared_task(ignore_result=True)
def daily_reminder():
    creators = User.query.join(User.roles).filter(Role.id == 2).all()
    general_users = User.query.join(User.roles).filter(Role.id == 3).all()
    users = list(set(creators + general_users))
    current_date = datetime.now().date
    for user in users:
        if user.current_login_at is not None:
            if user.current_login_at.date != current_date:
                send_message(user.email, "Reminder", "Daily Reminder")
    return "Reminder sent!"


@shared_task(ignore_result=True)
def creator_report():
    creators = User.query.join(User.roles).filter(Role.id == 2).all()
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    songs_added = []
    songs_rating = []
    songs_played = 0
    for creator in creators:
        for song in creator.songs:
            if song.date_added.date() >= thirty_days_ago:
                songs_added.append(song)
                songs_rating.append(song.rating)
                songs_played += song.played
        rating = round((sum(songs_rating) / len(songs_rating)), 2)
        with open(creator_report_path, "r") as f:
            template = Template(f.read())
            send_message(
                creator.email,
                "Monthly Report",
                template.render(
                    creator=creator,
                    songs=songs_added,
                    rating=rating,
                    streams=songs_played,
                ),
            )
    return "Report Sent"
