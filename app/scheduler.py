import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask_apscheduler import APScheduler

from .email import send_streak_reminder

scheduler = APScheduler()

AWST = ZoneInfo("Australia/Perth")
logger = logging.getLogger(__name__)


@scheduler.task("cron", id="streak_reminder", hour=20, minute=0, timezone=AWST)
def streak_reminder_job():
    from .models import RegisteredUser

    today = datetime.now(AWST).date()

    users = RegisteredUser.query.filter(RegisteredUser.streak >= 2).all()

    for user in users:
        if user.last_active is None:
            continue

        last = user.last_active
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)

        if last.astimezone(AWST).date() < today:
            try:
                send_streak_reminder(user)
            except Exception:
                logger.exception("Failed to send streak reminder to user %s", user.id)
