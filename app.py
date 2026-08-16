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

    def show_totals(self, final=False):
        label = "Final totals" if final else "Today's totals"
        print(f"\n📊 {label}:")
        print(f"Protein:  {self.consumed_protein}g / {self.protein}g")
        print(f"Carbs:    {self.consumed_carbs}g / {self.carbs}g")
        print(f"Fat:      {self.consumed_fat}g / {self.fat}g")
        print(f"Calories: {self.consumed_calories} / {self.calories}")

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
                self.show_totals()
            else:
                print("Food not found.")

coach = NutritionCoach()

coach.greet()
coach.log_meal()