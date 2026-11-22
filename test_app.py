import json
import os
import tempfile
import unittest
from datetime import date

from app import NutritionCoach, match_food


def scripted_input(responses):
    prompts = []
    remaining = iter(responses)

    def _input(prompt=""):
        prompts.append(prompt)
        return next(remaining)

    return _input, prompts


class MatchFoodTests(unittest.TestCase):
    def test_exact_match_is_case_insensitive(self):
        match = match_food("premier protein shake")

        self.assertIsNotNone(match)
        self.assertEqual(match["kind"], "exact")
        self.assertEqual(match["name"], "Premier Protein Shake")
        self.assertEqual(match["info"]["protein"], 30)

    def test_partial_name_suggests_closest_food(self):
        match = match_food("kirkland bar")

        self.assertIsNotNone(match)
        self.assertEqual(match["kind"], "fuzzy")
        self.assertEqual(match["name"], "Kirkland Protein Bar")

    def test_unknown_food_has_no_match(self):
        self.assertIsNone(match_food("pizza"))
        self.assertIsNone(match_food("xyzzy"))


class LogMealTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.temp_dir.name, "daily_log.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def make_coach(self, responses):
        input_func, prompts = scripted_input(responses)
        coach = NutritionCoach(log_file=self.log_path, input_func=input_func)
        return coach, prompts

    def test_exact_match_logs_without_confirmation(self):
        coach, prompts = self.make_coach(["Premier Protein Shake", "done"])

        coach.log_meal()

        self.assertFalse(any("Did you mean" in prompt for prompt in prompts))
        self.assertEqual(coach.consumed_protein, 30)
        self.assertEqual(coach.consumed_carbs, 5)
        self.assertEqual(coach.consumed_fat, 3)
        self.assertEqual(coach.consumed_calories, 160)
        with open(self.log_path) as f:
            saved = json.load(f)
        self.assertEqual(saved["date"], date.today().isoformat())
        self.assertEqual(saved["consumed_protein"], 30)
        self.assertEqual(saved["consumed_calories"], 160)

        def fail_input(prompt=""):
            raise AssertionError("reloading the log should not ask for input")

        reloaded = NutritionCoach(log_file=self.log_path, input_func=fail_input)
        self.assertEqual(reloaded.consumed_protein, 30)
        self.assertEqual(reloaded.consumed_calories, 160)

    def test_confirmed_partial_match_is_logged(self):
        coach, prompts = self.make_coach(["kirkland bar", "yes", "done"])

        coach.log_meal()

        self.assertTrue(any('Did you mean "Kirkland Protein Bar"?' in prompt for prompt in prompts))
        self.assertEqual(coach.consumed_protein, 21)
        self.assertEqual(coach.consumed_carbs, 23)
        self.assertEqual(coach.consumed_fat, 7)
        self.assertEqual(coach.consumed_calories, 190)

    def test_declined_suggestion_logs_nothing_and_asks_again(self):
        coach, prompts = self.make_coach(["kirkland bar", "no", "done"])

        coach.log_meal()

        self.assertTrue(any('Did you mean "Kirkland Protein Bar"?' in prompt for prompt in prompts))
        self.assertEqual(coach.consumed_protein, 0)
        self.assertEqual(coach.consumed_carbs, 0)
        self.assertEqual(coach.consumed_fat, 0)
        self.assertEqual(coach.consumed_calories, 0)
        self.assertFalse(os.path.exists(self.log_path))
        self.assertGreaterEqual(len(prompts), 3)

    def test_unknown_food_is_not_logged(self):
        coach, prompts = self.make_coach(["pizza", "done"])

        coach.log_meal()

        self.assertFalse(any("Did you mean" in prompt for prompt in prompts))
        self.assertEqual(coach.consumed_protein, 0)
        self.assertEqual(coach.consumed_calories, 0)
        self.assertFalse(os.path.exists(self.log_path))


if __name__ == "__main__":
    unittest.main()
