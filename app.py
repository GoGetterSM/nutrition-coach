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

    def greet(self):
        print("=" * 40)
        print("🥗 Nutrition Coach")
        print("=" * 40)

    def log_meal(self):
        meal = input("\n🍽️ What did you eat today? ")

        food = None
        for name, info in foods.items():
            if name.lower() == meal.lower():
                food = info
                break

        if food:
            print(f"Protein: {food['protein']}")
            print(f"Carbs: {food['carbs']}")
            print(f"Fat: {food['fat']}")
            print(f"Calories: {food['calories']}")
        else:
            print("Food not found.")

coach = NutritionCoach()

coach.greet()
coach.log_meal()