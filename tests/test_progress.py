import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from app.routes import _update_user_progress

LOCAL_TZ = ZoneInfo("Australia/Perth")


def _make_user(*, last_active=None, streak=0, xp=0, level=1):
    """Build a lightweight stand-in for a RegisteredUser row."""
    return SimpleNamespace(
        last_active=last_active,
        streak=streak,
        xp=xp,
        level=level,
    )


class UpdateUserProgressTests(unittest.TestCase):
    """Tests for streak, XP, and level changes after completing a quiz."""

    def test_first_quiz_sets_streak_to_one(self):
        user = _make_user(last_active=None, streak=0)
        _update_user_progress(user, correct_count=3)
        self.assertEqual(user.streak, 1)

    def test_consecutive_day_increments_streak(self):
        yesterday_local = datetime.now(LOCAL_TZ) - timedelta(days=1)
        user = _make_user(
            last_active=yesterday_local.astimezone(timezone.utc),
            streak=4,
        )
        _update_user_progress(user, correct_count=5)
        self.assertEqual(user.streak, 5)

    def test_gap_of_two_days_resets_streak_to_one(self):
        two_days_ago_local = datetime.now(LOCAL_TZ) - timedelta(days=2)
        user = _make_user(
            last_active=two_days_ago_local.astimezone(timezone.utc),
            streak=10,
        )
        _update_user_progress(user, correct_count=2)
        self.assertEqual(user.streak, 1)

    def test_same_day_does_not_change_streak(self):
        earlier_today_local = datetime.now(LOCAL_TZ) - timedelta(hours=1)
        user = _make_user(
            last_active=earlier_today_local.astimezone(timezone.utc),
            streak=7,
        )
        _update_user_progress(user, correct_count=4)
        self.assertEqual(user.streak, 7)

    def test_correct_answers_add_ten_xp_each(self):
        user = _make_user(xp=50)
        _update_user_progress(user, correct_count=4)
        # 50 + (4 * 10) = 90
        self.assertEqual(user.xp, 90)

    def test_crossing_xp_threshold_levels_up_and_returns_true(self):
        user = _make_user(xp=95, level=1)
        leveled_up = _update_user_progress(user, correct_count=1)
        # 95 + 10 = 105, crosses level 2 threshold (100)
        self.assertEqual(user.level, 2)
        self.assertTrue(leveled_up)

    def test_no_level_change_returns_false(self):
        user = _make_user(xp=50, level=1)
        leveled_up = _update_user_progress(user, correct_count=1)
        self.assertEqual(user.level, 1)
        self.assertFalse(leveled_up)

    def test_last_active_updates_to_current_time(self):
        user = _make_user(last_active=None)
        before = datetime.now(timezone.utc)
        _update_user_progress(user, correct_count=1)
        after = datetime.now(timezone.utc)
        self.assertIsNotNone(user.last_active)
        self.assertGreaterEqual(user.last_active, before)
        self.assertLessEqual(user.last_active, after)


if __name__ == "__main__":
    unittest.main()
