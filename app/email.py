import logging
import threading

import resend
from flask import current_app
from markupsafe import escape

from .constants import ACHIEVEMENTS, LEVEL_TITLES

logger = logging.getLogger(__name__)


def _send(to: str, subject: str, html: str) -> None:
    app = current_app._get_current_object()

    def _task():
        with app.app_context():
            if not app.config.get("RESEND_API_KEY"):
                return
            try:
                resend.api_key = app.config["RESEND_API_KEY"]
                resend.Emails.send(
                    {
                        "from": app.config["RESEND_FROM"],
                        "to": to,
                        "subject": subject,
                        "html": html,
                    }
                )
            except Exception:
                logger.exception("Failed to send email to %s", to)

    threading.Thread(target=_task, daemon=True).start()


def send_streak_reminder(user) -> None:
    first_name = escape(user.first_name)
    _send(
        to=user.email,
        subject=f"Your {user.streak}-day streak is on thin ice 🧊",
        html=f"""
        <p>Hey {first_name},</p>
        <p>
            You've been on a <strong>{user.streak}-day streak</strong> and your quokka
            is starting to worry. Don't let it end today — one quick quiz is all it takes.
        </p>
        <p>— The Quokka Quiz crew 🦘</p>
        """,
    )


def send_achievement_unlocked(user, achievement_key: str) -> None:
    achievement = ACHIEVEMENTS.get(achievement_key)
    if not achievement:
        return

    first_name = escape(user.first_name)
    _send(
        to=user.email,
        subject=f"You just earned '{achievement['name']}' — look at you go 🏅",
        html=f"""
        <p>Hey {first_name},</p>
        <p>
            You just unlocked the <strong>{achievement['name']}</strong> badge
            ({achievement['description']}). Your quokka ({achievement['quokka']}) is
            officially impressed.
        </p>
        <p>— The Quokka Quiz crew 🦘</p>
        """,
    )


def send_level_up(user) -> None:
    title = LEVEL_TITLES.get(user.level, "Quiz Legend")

    first_name = escape(user.first_name)
    _send(
        to=user.email,
        subject=f"Ding! You're now a {title} 🎉",
        html=f"""
        <p>Hey {first_name},</p>
        <p>
            Level up! You've reached <strong>Level {user.level}: {title}</strong>.
            Your brain is visibly getting bigger and your quokka couldn't be prouder.
        </p>
        <p>— The Quokka Quiz crew 🦘</p>
        """,
    )
