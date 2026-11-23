import json
from datetime import date
from difflib import get_close_matches

foods = {
    "Premier Protein Shake": {
        "protein": 30,
        "carbs": 5,
        "fat": 3,
        "calories": 160
    },

    "Kirkland Protein Bar": {
        "protein": 21,
        "carbs": 23,
        "fat": 7,
        "calories": 190
    }
}

DAILY_LOG_FILE = "daily_log.json"

# difflib's default cutoff. "kirkland bar" scores about 0.75 against
# "Kirkland Protein Bar"; unrelated names such as "pizza" stay well below.
FUZZY_MATCH_CUTOFF = 0.6


def _normalize(text):
    return " ".join(text.lower().split())


def match_food(query, catalog=None):
    """Return the food entry for a query.

    Exact case-insensitive names win immediately. Otherwise the closest
    catalog name above FUZZY_MATCH_CUTOFF is returned as a suggestion.
    """
    catalog = foods if catalog is None else catalog
    normalized = _normalize(query)
    if not normalized:
        return None

    by_name = {}
    for name, info in catalog.items():
        by_name[_normalize(name)] = (name, info)

    if normalized in by_name:
        name, info = by_name[normalized]
        return {"kind": "exact", "name": name, "info": info}

    suggestions = get_close_matches(
        normalized,
        list(by_name),
        n=1,
        cutoff=FUZZY_MATCH_CUTOFF,
    )
    if not suggestions:
        return None

    name, info = by_name[suggestions[0]]
    return {"kind": "fuzzy", "name": name, "info": info}


class NutritionCoach:

    def __init__(self, log_file=None, input_func=None):
        self.protein = 160
        self.carbs = 170
        self.fat = 55
        self.calories = 1815
        self.consumed_protein = 0
        self.consumed_carbs = 0
        self.consumed_fat = 0
        self.consumed_calories = 0
        self.log_file = log_file or DAILY_LOG_FILE
        self._input = input_func or input
        self.load_daily_log()

    def load_daily_log(self):
        try:
            with open(self.log_file) as f:
                data = json.load(f)
            if data.get("date") != date.today().isoformat():
                return
            self.consumed_protein = data["consumed_protein"]
            self.consumed_carbs = data["consumed_carbs"]
            self.consumed_fat = data["consumed_fat"]
            self.consumed_calories = data["consumed_calories"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            pass

    def show_totals(self, final=False):
        label = "Final totals" if final else "Today's totals"
        print(f"\n📊 {label}:")
        print(f"Protein:  {self.consumed_protein}g / {self.protein}g")
        print(f"Carbs:    {self.consumed_carbs}g / {self.carbs}g")
        print(f"Fat:      {self.consumed_fat}g / {self.fat}g")
        print(f"Calories: {self.consumed_calories} / {self.calories}")

    def save_daily_log(self):
        data = {
            "date": date.today().isoformat(),
            "consumed_protein": self.consumed_protein,
            "consumed_carbs": self.consumed_carbs,
            "consumed_fat": self.consumed_fat,
            "consumed_calories": self.consumed_calories,
        }
        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=2)

    def greet(self):
        print("=" * 40)
        print("🥗 Nutrition Coach")
        print("=" * 40)

    def _confirm_match(self, name):
        while True:
            answer = self._input(f'Did you mean "{name}"? (yes/no) ').strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer yes or no.")

    def _log_food(self, food):
        print(f"Protein: {food['protein']}g")
        print(f"Carbs: {food['carbs']}g")
        print(f"Fat: {food['fat']}g")
        print(f"Calories: {food['calories']}")
        self.consumed_protein += food["protein"]
        self.consumed_carbs += food["carbs"]
        self.consumed_fat += food["fat"]
        self.consumed_calories += food["calories"]
        self.save_daily_log()
        self.show_totals()

    def log_meal(self):
        while True:
            meal = self._input("\n🍽️ What did you eat today? (type 'done' to finish) ").strip()

            if meal.lower() == "done":
                self.show_totals(final=True)
                break

            match = match_food(meal)
            if match is None:
                print("Food not found.")
                continue

            if match["kind"] == "fuzzy" and not self._confirm_match(match["name"]):
                print("Okay, nothing logged.")
                continue

            self._log_food(match["info"])


def main():
    coach = NutritionCoach()
    coach.greet()
    coach.log_meal()


if __name__ == "__main__":
    main()
