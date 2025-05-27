# Imports
import requests # For making API calls
import tkinter as tk # For GUI diisplay
import random # For selecting a random joke

# Get meal data from API
def get_meal(keyword):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={keyword}"
    respose = requests.get(url)
    data = response.json()

    # Check if a meal is found
    if data["meals"] is None:
        return None
    
    meal = data["meals"][0]  # Select first meal

    # Get meal details with default values if missing
    name = meal.get("strMeal", "N/A")
    category = meal.get("strCategory", "N/A")
    area = meal.get("strArea", "N/A")

    # Find two ingredients
    ingredients = [meal.get(f"strIngredient{i}", "N/A").strip() for i in range(1, 21) if meal.get(f"strIngredient{i}")]
    ingredients = ingredients[:2] if len(ingredients) >= 2 else ingredients + ["N/A"] * (2 - len(ingredients))

    return {
        "name": name,
        "category": category,
        "area": area,
        "ingredient1": ingredients[0],
        "ingredient2": ingredients[1]
    }

# Fetch jokes from API
def get_food_joke():
    all_jokes = []
    for _ in range(3):  # Get ~30 jokes
        response = requests.get("https://official-joke-api.appspot.com/jokes/ten")
        all_jokes.extend(response.json())

        # Filter jokes related to food
        food_words = ["food", "eat", "meal", "chicken", "pizza", "burger", "hungry", "cook", "kitchen"]
        food_jokes = [j for j in all_jokes if any(word in (j["setup"] + j["punchline"]).lower() for word in food_words)]

        # Select a joke
        joke = random.choice(food_jokes) if food_jokes else random.choice(all_jokes)
        return joke["setup"], joke["punchline"]

# Get user input
def show_info():
    keyword = entry.get().strip()
    if not keyword:
        output.set("Please enter a meal or ingredient keyword.")
        return

    # Get meal details
    meal = get_meal(keyword)
    if meal is None:
        output.set(f"No meals found for '{keyword}'. Try another keyword.")
        return

    # Get a food related joke
    setup, punchline = get_food_joke()

    # Display meal info and joke
    text = (
        f"Meal Name: {meal['name']}\n"
        f"Category: {meal['category']}\n"
        f"Cuisine: {meal['area']}\n"
        f"Main Ingredient 1: {meal['ingredient1']}\n"
        f"Main Ingredient 2: {meal['ingredient2']}\n\n"
        "Here's a food-related joke for you:\n"
        f"{setup}\n{punchline}"
    )
    output.set(text)

    # Set up GUI window
    root = tk.Tk()
    root.title("Meal & Food Joke Finder")
    root.geometry("600x400")

    tk.Label(root, text="Enter meal or ingredient:", font=("Arial", 14)).pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(pady=5, fill='x', padx=20)

    btn = tk.Button(root, text="Get Meal & Joke", font=("Arial", 14), command=show_info)
    btn.pack(pady=10)

    output = tk.StringVar()
    label = tk.Label(root, textvariable=output, font=("Arial", 12), justify="left", wraplength=560)
    label.pack(padx=20, pady=10)

    root.mainloop()

    