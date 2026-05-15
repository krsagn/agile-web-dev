import unittest

from app.routes import _calculate_level, _next_level_xp


class CalculateLevelTests(unittest.TestCase):
    """Tests for the XP-to-level calculation."""

    def test_zero_xp_returns_level_one(self):
        self.assertEqual(_calculate_level(0), 1)

    def test_xp_just_below_level_two_threshold_stays_at_level_one(self):
        self.assertEqual(_calculate_level(99), 1)

    def test_exactly_meeting_threshold_moves_to_next_level(self):
        self.assertEqual(_calculate_level(100), 2)

    def test_mid_range_xp_returns_correct_level(self):
        # 1000 XP is the level 5 threshold
        self.assertEqual(_calculate_level(1000), 5)

    def test_xp_at_max_level_threshold_returns_level_ten(self):
        self.assertEqual(_calculate_level(5000), 10)

    def test_xp_beyond_max_level_caps_at_level_ten(self):
        self.assertEqual(_calculate_level(99_999), 10)


class NextLevelXpTests(unittest.TestCase):
    """Tests for the XP required to reach the next level."""

    def test_next_xp_from_level_one_is_one_hundred(self):
        self.assertEqual(_next_level_xp(1), 100)

    def test_next_xp_from_mid_level_returns_correct_threshold(self):
        # From level 5 the next is level 6 at 1500 XP
        self.assertEqual(_next_level_xp(5), 1500)

    def test_next_xp_at_max_level_returns_max_threshold(self):
        # No level above 10 — function returns the level 10 threshold itself
        self.assertEqual(_next_level_xp(10), 5000)

    def test_next_xp_for_unknown_level_returns_zero(self):
        self.assertEqual(_next_level_xp(99), 0)


if __name__ == "__main__":
    unittest.main()
