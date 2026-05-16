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
        # Additional diverse users for leaderboard testing
        _make_user(
            "Frank",
            "Williams",
            "frank",
            "frank@example.com",
            xp=0,
            level=0,
            streak=0,
            days_ago_active=999,  # Never active (brand new account)
        ),
        _make_user(
            "Grace",
            "Chen",
            "grace",
            "grace@example.com",
            xp=5500,
            level=12,
            streak=45,
            days_ago_active=0,  # Active today, top scorer
        ),
        _make_user(
            "Henry",
            "Martinez",
            "henry",
            "henry@example.com",
            xp=800,
            level=4,
            streak=0,
            days_ago_active=3,  # Broken streak (hasn't played in 3 days)
        ),
        _make_user(
            "Iris",
            "Patel",
            "iris",
            "iris@example.com",
            xp=200,
            level=2,
            streak=2,
            days_ago_active=1,  # Ready for today's quiz
        ),
        _make_user(
            "Jack",
            "Wilson",
            "jack",
            "jack@example.com",
            xp=3200,
            level=9,
            streak=8,
            days_ago_active=0,  # Active today, high level
        ),
        _make_user(
            "Karen",
            "Brown",
            "karen",
            "karen@example.com",
            xp=650,
            level=3,
            streak=5,
            days_ago_active=2,  # Ready for today's quiz
        ),
        _make_user(
            "Leo",
            "Garcia",
            "leo",
            "leo@example.com",
            xp=1100,
            level=5,
            streak=0,
            days_ago_active=10,  # Inactive for 10 days, broken streak
        ),
        _make_user(
            "Megan",
            "Davis",
            "megan",
            "megan@example.com",
            xp=400,
            level=2,
            streak=1,
            days_ago_active=1,  # Ready for today's quiz
        ),
        _make_user(
            "Nathan",
            "Rodriguez",
            "nathan",
            "nathan@example.com",
            xp=2100,
            level=7,
            streak=15,
            days_ago_active=0,  # Active today, strong player
        ),
        _make_user(
            "Olivia",
            "Anderson",
            "olivia",
            "olivia@example.com",
            xp=50,
            level=1,
            streak=0,
            days_ago_active=999,  # Never active (brand new account)
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
        # Frank — no results (brand new account)
        # Grace — very high scorer, active today
        _make_result(users[6], "Math", 10, 10, 45, days_ago=0),
        _make_result(users[6], "Science", 10, 10, 50, days_ago=1),
        _make_result(users[6], "Programming", 10, 10, 42, days_ago=2),
        _make_result(users[6], "History", 10, 10, 48, days_ago=3),
        # Henry — broken streak (hasn't played in 3 days)
        _make_result(users[7], "Math", 7, 10, 150, days_ago=3),
        _make_result(users[7], "Programming", 8, 10, 120, days_ago=4),
        _make_result(users[7], "Science", 6, 10, 180, days_ago=5),
        # Iris — ready for today's quiz, played yesterday
        _make_result(users[8], "Science", 5, 10, 280, days_ago=1),
        _make_result(users[8], "Math", 6, 10, 260, days_ago=2),
        # Jack — high level player, active today
        _make_result(users[9], "Programming", 10, 10, 65, days_ago=0),
        _make_result(users[9], "Math", 9, 10, 75, days_ago=1),
        _make_result(users[9], "Science", 9, 10, 82, days_ago=2),
        _make_result(users[9], "History", 8, 10, 95, days_ago=3),
        # Karen — ready for today's quiz, played 2 days ago
        _make_result(users[10], "Math", 7, 10, 140, days_ago=2),
        _make_result(users[10], "Science", 6, 10, 165, days_ago=3),
        _make_result(users[10], "Programming", 7, 10, 155, days_ago=4),
        # Leo — inactive for 10 days, broken streak
        _make_result(users[11], "Science", 8, 10, 130, days_ago=10),
        _make_result(users[11], "Math", 7, 10, 145, days_ago=11),
        _make_result(users[11], "Programming", 9, 10, 110, days_ago=12),
        # Megan — ready for today's quiz, played yesterday
        _make_result(users[12], "History", 5, 10, 320, days_ago=1),
        _make_result(users[12], "Science", 6, 10, 290, days_ago=2),
        # Nathan — strong player, active today
        _make_result(users[13], "Math", 9, 10, 70, days_ago=0),
        _make_result(users[13], "Science", 9, 10, 68, days_ago=1),
        _make_result(users[13], "Programming", 8, 10, 85, days_ago=2),
        _make_result(users[13], "History", 9, 10, 92, days_ago=3),
        # Olivia — no results (brand new account)
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
        # Grace — top scorer with multiple achievements
        UserAchievement(
            user_id=users[6].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=45),
        ),
        UserAchievement(
            user_id=users[6].id,
            achievement_key="perfect_score",
            earned_at=datetime.now(timezone.utc) - timedelta(days=10),
        ),
        UserAchievement(
            user_id=users[6].id,
            achievement_key="speed_demon",
            earned_at=datetime.now(timezone.utc) - timedelta(days=5),
        ),
        UserAchievement(
            user_id=users[6].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=40),
        ),
        UserAchievement(
            user_id=users[6].id,
            achievement_key="streak_30",
            earned_at=datetime.now(timezone.utc) - timedelta(days=20),
        ),
        UserAchievement(
            user_id=users[6].id,
            achievement_key="math_genius",
            earned_at=datetime.now(timezone.utc) - timedelta(days=3),
        ),
        # Henry — moderate achievements
        UserAchievement(
            user_id=users[7].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=8),
        ),
        UserAchievement(
            user_id=users[7].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=4),
        ),
        # Iris — new player, first quiz achievement
        UserAchievement(
            user_id=users[8].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        # Jack — strong player achievements
        UserAchievement(
            user_id=users[9].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=20),
        ),
        UserAchievement(
            user_id=users[9].id,
            achievement_key="perfect_score",
            earned_at=datetime.now(timezone.utc) - timedelta(days=2),
        ),
        UserAchievement(
            user_id=users[9].id,
            achievement_key="speed_demon",
            earned_at=datetime.now(timezone.utc),
        ),
        UserAchievement(
            user_id=users[9].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=15),
        ),
        # Karen — moderate player
        UserAchievement(
            user_id=users[10].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=6),
        ),
        UserAchievement(
            user_id=users[10].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=1),
        ),
        # Leo — inactive player, older achievements
        UserAchievement(
            user_id=users[11].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=20),
        ),
        UserAchievement(
            user_id=users[11].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=18),
        ),
        # Megan — new player
        UserAchievement(
            user_id=users[12].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=2),
        ),
        # Nathan — strong player achievements
        UserAchievement(
            user_id=users[13].id,
            achievement_key="first_quiz",
            earned_at=datetime.now(timezone.utc) - timedelta(days=18),
        ),
        UserAchievement(
            user_id=users[13].id,
            achievement_key="perfect_score",
            earned_at=datetime.now(timezone.utc) - timedelta(days=5),
        ),
        UserAchievement(
            user_id=users[13].id,
            achievement_key="speed_demon",
            earned_at=datetime.now(timezone.utc) - timedelta(days=2),
        ),
        UserAchievement(
            user_id=users[13].id,
            achievement_key="streak_7",
            earned_at=datetime.now(timezone.utc) - timedelta(days=12),
        ),
    ]

    db.session.add_all(achievements)
    db.session.commit()

    click.echo("")
    click.echo("Database seeded. 15 users, 44 quiz results, 44 achievements.")
    click.echo("")
    click.echo("  Username  Password     Level  XP    Streak  Activity")
    click.echo("  --------  -----------  -----  ----  ------  ---------------------")
    click.echo("  alice     password123  6      1520  12      Active today ✓")
    click.echo("  bob       password123  3      450   3       Played yesterday")
    click.echo("  carol     password123  3      310   0       Inactive 5 days (streak broken)")
    click.echo("  dave      password123  8      2850  30      Active today ✓")
    click.echo("  eve       password123  1      90    1       Active today ✓")
    click.echo("  frank     password123  0      0     0       Brand new (never active)")
    click.echo("  grace     password123  12     5500  45      Active today ✓ (top scorer)")
    click.echo("  henry     password123  4      800   0       Inactive 3 days (streak broken)")
    click.echo("  iris      password123  2      200   2       Ready for today ✓")
    click.echo("  jack      password123  9      3200  8       Active today ✓")
    click.echo("  karen     password123  3      650   5       Ready for today ✓")
    click.echo("  leo       password123  5      1100  0       Inactive 10 days (streak broken)")
    click.echo("  megan     password123  2      400   1       Ready for today ✓")
    click.echo("  nathan    password123  7      2100  15      Active today ✓")
    click.echo("  olivia    password123  1      50    0       Brand new (never active)")
    click.echo("")
    click.echo("Ready to attempt today's quiz (haven't played today):")
    click.echo("  • iris, karen, megan")
    click.echo("")
    click.echo("Already played today (6 users):")
    click.echo("  • alice, dave, eve, grace, jack, nathan")
    click.echo("")
    click.echo("Leaderboard range:")
    click.echo("  • XP: 0 to 5500 | Levels: 0 to 12 | Streaks: 0 to 45")
    click.echo("  • Includes edge cases: brand new accounts, inactive/broken streaks, consistent top performers")
    click.echo("")


@click.command("reset-db")
@with_appcontext
def reset_db_command():
    """Clear all user data from the database."""
    _clear_all()
    click.echo("Database cleared.")
