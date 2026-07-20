from django.test import TestCase
import unittest
from types import SimpleNamespace


class ManagementSystemTests(unittest.TestCase):
    def test_resolve_current_username_prefers_current_user_without_username_attribute(self):
        engine = ManagementSystem("dummy.db")
        engine.current_user = "acronims"

        self.assertEqual(engine.get_current_username(), "acronims")

    def test_resolve_current_username_falls_back_when_no_user_is_set(self):
        engine = ManagementSystem("dummy.db")

        self.assertEqual(engine.get_current_username(), "Unknown")

    def test_priority_score_prefers_tv_over_video_and_film(self):
        engine = ManagementSystem("dummy.db")

        tv_proposal = SimpleNamespace(
            title="The Launch",
            project_type="TV series",
            genre="Drama",
            duration=3,
            budget=50000,
            description="A strong pilot",
        )
        video_proposal = SimpleNamespace(
            title="Short Promo",
            project_type="Video",
            genre="Comedy",
            duration=2,
            budget=40000,
            description="A short-form piece",
        )
        film_proposal = SimpleNamespace(
            title="A Very Long Film Title That Should Score Lower",
            project_type="Film",
            genre="Action",
            duration=6,
            budget=80000,
            description="A long feature",
        )

        self.assertGreater(engine.priority_score(tv_proposal), engine.priority_score(video_proposal))
        self.assertGreater(engine.priority_score(video_proposal), engine.priority_score(film_proposal))


if __name__ == "__main__":
    unittest.main()
