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

# Fetch jokes from API

# Filter jokes realted to food

# Select a joke

# Get meal details

# Get a food related joke

# Display meal info and joke

# Set up GUI window