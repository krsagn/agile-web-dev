import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from app import create_app
from app.config import TestingConfig
from app.db import QuizResult
from app.models import RegisteredUser, UserAchievement, db
from app.routes import _achievement_unlocked, _unlock_achievements


def _result(score=10, total=10, time_taken=60, category="Science"):
    return SimpleNamespace(
        score=score, total=total, time_taken=time_taken, category=category
    )


def _user(streak=0, quiz_results=None, achievements=None):
    return SimpleNamespace(
        streak=streak,
        quiz_results=quiz_results or [],
        achievements=achievements or [],
    )


class AchievementUnlockedTests(unittest.TestCase):
    """Pure boolean checks — does a given achievement key apply to this result?"""

    def test_first_quiz_unlocked_when_user_has_a_quiz_result(self):
        user = _user(quiz_results=[object()])
        self.assertTrue(_achievement_unlocked("first_quiz", user, _result(), 10))

    def test_perfect_score_unlocked_when_all_correct(self):
        self.assertTrue(
            _achievement_unlocked("perfect_score", _user(), _result(score=10, total=10), 10)
        )

    def test_perfect_score_not_unlocked_when_one_wrong(self):
        self.assertFalse(
            _achievement_unlocked("perfect_score", _user(), _result(score=9, total=10), 9)
        )

    def test_speed_demon_unlocked_at_exactly_two_minutes(self):
        self.assertTrue(
            _achievement_unlocked("speed_demon", _user(), _result(time_taken=120), 0)
        )

    def test_speed_demon_not_unlocked_above_two_minutes(self):
        self.assertFalse(
            _achievement_unlocked("speed_demon", _user(), _result(time_taken=121), 0)
        )

    def test_streak_seven_requires_seven_day_streak(self):
        self.assertTrue(_achievement_unlocked("streak_7", _user(streak=7), _result(), 0))
        self.assertFalse(_achievement_unlocked("streak_7", _user(streak=6), _result(), 0))

    def test_category_specific_requires_matching_category_and_perfect_score(self):
        perfect_science = _result(score=10, total=10, category="Science")
        self.assertTrue(_achievement_unlocked("science_ace", _user(), perfect_science, 10))

        imperfect_science = _result(score=9, total=10, category="Science")
        self.assertFalse(_achievement_unlocked("science_ace", _user(), imperfect_science, 9))

        perfect_math = _result(score=10, total=10, category="Math")
        self.assertFalse(_achievement_unlocked("science_ace", _user(), perfect_math, 10))

    def test_hundred_correct_triggers_at_one_hundred_correct_answers(self):
        self.assertTrue(_achievement_unlocked("hundred_correct", _user(), _result(), 100))
        self.assertFalse(_achievement_unlocked("hundred_correct", _user(), _result(), 99))


class UnlockAchievementsTests(unittest.TestCase):
    """End-to-end achievement unlocking using an in-memory DB."""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = RegisteredUser(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password_hash="x",
            terms_read=True,
            xp=0,
            level=1,
            streak=1,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _quiz_result(self, score=10, total=10, time_taken=60, category="Science"):
        return SimpleNamespace(
            score=score, total=total, time_taken=time_taken, category=category
        )

    def test_unlocks_new_achievement_for_perfect_quiz(self):
        # Simulating a freshly-completed quiz already in the user's history
        self.user.quiz_results.append(
            QuizResult(
                category="Science",
                score=10,
                total=10,
                time_taken=60,
                completed_at=datetime.now(timezone.utc),
            )
        )
        unlocked = _unlock_achievements(self.user, self._quiz_result())
        keys = {a["key"] for a in unlocked}
        self.assertIn("first_quiz", keys)
        self.assertIn("perfect_score", keys)

    def test_does_not_unlock_already_earned_achievement(self):
        self.user.achievements.append(
            UserAchievement(achievement_key="perfect_score", earned_at=datetime.now(timezone.utc))
        )
        self.user.quiz_results.append(
            QuizResult(
                category="Science",
                score=10,
                total=10,
                time_taken=60,
                completed_at=datetime.now(timezone.utc),
            )
        )
        unlocked = _unlock_achievements(self.user, self._quiz_result())
        keys = {a["key"] for a in unlocked}
        self.assertNotIn("perfect_score", keys)

    def test_multiple_achievements_unlock_in_one_quiz(self):
        # Perfect science quiz in under 2 minutes = perfect_score + speed_demon + science_ace + first_quiz
        self.user.quiz_results.append(
            QuizResult(
                category="Science",
                score=10,
                total=10,
                time_taken=60,
                completed_at=datetime.now(timezone.utc),
            )
        )
        unlocked = _unlock_achievements(
            self.user, self._quiz_result(time_taken=90, category="Science")
        )
        keys = {a["key"] for a in unlocked}
        self.assertIn("perfect_score", keys)
        self.assertIn("speed_demon", keys)
        self.assertIn("science_ace", keys)

    def test_imperfect_quiz_does_not_unlock_perfect_achievements(self):
        self.user.quiz_results.append(
            QuizResult(
                category="Science",
                score=8,
                total=10,
                time_taken=60,
                completed_at=datetime.now(timezone.utc),
            )
        )
        unlocked = _unlock_achievements(
            self.user, self._quiz_result(score=8, total=10, category="Science")
        )
        keys = {a["key"] for a in unlocked}
        self.assertNotIn("perfect_score", keys)
        self.assertNotIn("science_ace", keys)


if __name__ == "__main__":
    unittest.main()
