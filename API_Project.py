# Imports
import requests  # Import the requests module to make API calls
import tkinter as tk  # Import tkinter for creating a GUI window
import random  # Import the random module for selecting a joke randomly

# Function to get meal details from API
def get_meal(keyword):
    # Construct API URL using the provided keyword
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={keyword}"

    # Send a GET request to the API
    response = requests.get(url)

    # Convert API response into a JSON dictionary
    data = response.json()

    # Check if meals exist in the API response
    if data["meals"] is None:
        return None  # Return None if no meal is found

    # Select the first meal from the list
    meal = data["meals"][0]

    # Extract meal name, category, and cuisine type, using "N/A" if missing
    name = meal.get("strMeal") or "N/A"
    category = meal.get("strCategory") or "N/A"
    area = meal.get("strArea") or "N/A"

    # Initialize an empty list for ingredients
    ingredients = []

    # Loop through ingredient fields from 1 to 20
    for i in range(1, 21):
        ing = meal.get(f"strIngredient{i}")  # Retrieve ingredient i
        if ing and ing.strip():  # Check if ingredient exists and is non-empty
            ingredients.append(ing.strip())  # Add to ingredient list
        if len(ingredients) == 2:  # Stop after finding two ingredients
            break

    # Ensure the list contains exactly two ingredients (fill missing ones with "N/A")
    while len(ingredients) < 2:
        ingredients.append("N/A")

    # Return a dictionary containing meal details
    return {
        "name": name,
        "category": category,
        "area": area,
        "ingredient1": ingredients[0],
        "ingredient2": ingredients[1]
    }

# Function to retrieve a food-related joke
def get_food_joke():
    all_jokes = []  # Initialize a list to store jokes

    # Fetch jokes from API three times to get a larger selection (~30 jokes)
    for _ in range(3):
        response = requests.get("https://official-joke-api.appspot.com/jokes/ten")
        all_jokes.extend(response.json())  # Add retrieved jokes to the list

    # Define a list of food-related words to filter jokes
    food_words = ["food", "eat", "meal", "chicken", "pizza", "burger", "hungry", "cook", "kitchen"]

    # Filter jokes to find those related to food
    food_jokes = [j for j in all_jokes if any(word in (j["setup"] + j["punchline"]).lower() for word in food_words)]

    # Select a joke: Prefer food-related jokes, but use a random joke if none found
    joke = random.choice(food_jokes) if food_jokes else random.choice(all_jokes)

    # Return the setup and punchline of the joke
    return joke["setup"], joke["punchline"]

# Function to handle user input and display results
def show_info():
    # Retrieve user input from text field and remove leading/trailing spaces
    keyword = entry.get().strip()

    # If input is empty, prompt user to enter a valid keyword
    if not keyword:
        output.set("Please enter a meal or ingredient keyword.")
        return

    # Call get_meal function to retrieve meal details
    meal = get_meal(keyword)

    # If no meal is found, inform the user
    if meal is None:
        output.set(f"No meals found for '{keyword}'. Try another keyword.")
        return

    # Retrieve a food-related joke
    setup, punchline = get_food_joke()

    # Format the meal details and joke into a readable message
    text = (
        f"Meal Name: {meal['name']}\n"
        f"Category: {meal['category']}\n"
        f"Cuisine: {meal['area']}\n"
        f"Main Ingredient 1: {meal['ingredient1']}\n"
        f"Main Ingredient 2: {meal['ingredient2']}\n\n"
        "Here's a food-related joke for you:\n"
        f"{setup}\n{punchline}"
    )

    # Update the output display with meal details and joke
    output.set(text)

# Initialize GUI window
root = tk.Tk()  # Create main application window
root.title("Meal & Food Joke Finder")  # Set window title
root.geometry("600x400")  # Set window size

# Create label for user instructions
tk.Label(root, text="Enter meal or ingredient:", font=("Arial", 14)).pack(pady=10)

# Create text entry field for user input
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5, fill='x', padx=20)

# Create button to trigger meal search and joke retrieval
btn = tk.Button(root, text="Get Meal & Joke", font=("Arial", 14), command=show_info)
btn.pack(pady=10)

# Create variable to store the output message
output = tk.StringVar()

# Create label to display meal details and joke
label = tk.Label(root, textvariable=output, font=("Arial", 12), justify="left", wraplength=560)
label.pack(padx=20, pady=10)

# Start GUI event loop (runs the application)
root.mainloop()
