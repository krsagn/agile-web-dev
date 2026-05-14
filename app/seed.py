import click
from datetime import datetime, timezone, timedelta
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from .models import db, RegisteredUser, QuizResult, UserAchievement


def _clear_all():
    UserAchievement.query.delete()
    QuizResult.query.delete()
    RegisteredUser.query.delete()
    db.session.commit()


def _make_user(first, last, username, email, xp, level, streak, days_ago_active):
    return RegisteredUser(
        first_name=first,
        last_name=last,
        username=username,
        email=email,
        password_hash=generate_password_hash("password123"),
        terms_read=True,
        xp=xp,
        level=level,
        streak=streak,
        last_active=datetime.now(timezone.utc) - timedelta(days=days_ago_active),
        created_at=datetime.now(timezone.utc) - timedelta(days=30),
    )


def _make_result(user, category, score, total, time_taken, days_ago):
    return QuizResult(
        user_id=user.id,
        category=category,
        score=score,
        total=total,
        time_taken=time_taken,
        completed_at=datetime.now(timezone.utc) - timedelta(days=days_ago),
    )


@click.command("seed")
@with_appcontext
def seed_command():
    """Reset the database and populate it with dummy data."""
    _clear_all()

    users = [
        _make_user(
            "Alice",
            "Smith",
            "alice",
            "alice@example.com",
            xp=1520,
            level=6,
            streak=12,
            days_ago_active=0,
        ),
        _make_user(
            "Bob",
            "Jones",
            "bob",
            "bob@example.com",
            xp=450,
            level=3,
            streak=3,
            days_ago_active=1,
        ),
        _make_user(
            "Carol",
            "Lee",
            "carol",
            "carol@example.com",
            xp=310,
            level=3,
            streak=0,
            days_ago_active=5,
        ),
        _make_user(
            "Dave",
            "Nguyen",
            "dave",
            "dave@example.com",
            xp=2850,
            level=8,
            streak=30,
            days_ago_active=0,
        ),
        _make_user(
            "Eve",
            "Tanaka",
            "eve",
            "eve@example.com",
            xp=90,
            level=1,
            streak=1,
            days_ago_active=0,
        ),
    ]

    db.session.add_all(users)
    db.session.flush()

    results = [
        # Alice — active today, high scorer
        _make_result(users[0], "Science", 9, 10, 95, days_ago=0),
        _make_result(users[0], "Programming", 10, 10, 87, days_ago=1),
        _make_result(users[0], "Math", 8, 10, 110, days_ago=2),
        # Bob — played yesterday
        _make_result(users[1], "Math", 6, 10, 200, days_ago=1),
        _make_result(users[1], "Science", 7, 10, 175, days_ago=2),
        # Carol — hasn't played in 5 days, streak broken
        _make_result(users[2], "Programming", 5, 10, 300, days_ago=5),
        # Dave — active today, on a 30-day streak
        _make_result(users[3], "Math", 10, 10, 60, days_ago=0),
        _make_result(users[3], "Science", 10, 10, 55, days_ago=1),
        _make_result(users[3], "Programming", 9, 10, 72, days_ago=2),
        # Eve — first quiz today
        _make_result(users[4], "Science", 4, 10, 420, days_ago=0),
    ]

    db.session.add_all(results)
    db.session.flush()

    achievements = [
        UserAchievement(
            user_id=users[0].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=10),
        ),
        UserAchievement(
            user_id=users[0].id,
            achievement_key="perfect_score",
            earned_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        UserAchievement(
            user_id=users[0].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=5),
        ),
        UserAchievement(
            user_id=users[1].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=3),
        ),
        UserAchievement(
            user_id=users[2].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=5),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=25),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="perfect_score",
            earned_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="speed_demon",
            earned_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=23),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="streak_30",
            earned_at=datetime.now(timezone.utc),
        ),
        UserAchievement(
            user_id=users[3].id,
            achievement_key="math_genius",
            earned_at=datetime.now(timezone.utc),
        ),
        UserAchievement(
            user_id=users[4].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc),
        ),
    ]

    db.session.add_all(achievements)
    db.session.commit()

    click.echo("")
    click.echo("Database seeded. 5 users, 10 quiz results, 12 achievements.")
    click.echo("")
    click.echo("  Username  Password     Level  XP    Streak")
    click.echo("  --------  -----------  -----  ----  ------")
    click.echo("  alice     password123  6      1520  12")
    click.echo("  bob       password123  3      450   3")
    click.echo("  carol     password123  3      310   0")
    click.echo("  dave      password123  8      2850  30")
    click.echo("  eve       password123  1      90    1")
    click.echo("")
    click.echo("  alice and dave have completed today's quiz.")
    click.echo("  carol has not played in 5 days (streak broken).")
    click.echo("")


@click.command("reset-db")
@with_appcontext
def reset_db_command():
    """Clear all user data from the database."""
    _clear_all()
    click.echo("Database cleared.")
