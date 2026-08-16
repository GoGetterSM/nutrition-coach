import json
from datetime import date

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

class NutritionCoach:

    def __init__(self):
        self.protein = 160
        self.carbs = 170
        self.fat = 55
        self.calories = 1815
        self.consumed_protein = 0
        self.consumed_carbs = 0
        self.consumed_fat = 0
        self.consumed_calories = 0
        self.load_daily_log()

    def load_daily_log(self):
        try:
            with open(DAILY_LOG_FILE) as f:
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
        with open(DAILY_LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def greet(self):
        print("=" * 40)
        print("🥗 Nutrition Coach")
        print("=" * 40)

    def log_meal(self):
        while True:
            meal = input("\n🍽️ What did you eat today? (type 'done' to finish) ")

            if meal.lower() == "done":
                self.show_totals(final=True)
                break

            food = None
            for name, info in foods.items():
                if name.lower() == meal.lower():
                    food = info
                    break

            if food:
                print(f"Protein: {food['protein']}g")
                print(f"Carbs: {food['carbs']}g")
                print(f"Fat: {food['fat']}g")
                print(f"Calories: {food['calories']}")
                self.consumed_protein += food['protein']
                self.consumed_carbs += food['carbs']
                self.consumed_fat += food['fat']
                self.consumed_calories += food['calories']
                self.save_daily_log()
                self.show_totals()
            else:
                print("Food not found.")

coach = NutritionCoach()

coach.greet()
coach.log_meal()