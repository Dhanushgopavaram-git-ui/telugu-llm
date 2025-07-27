import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# Function to print recipe details with nutrition information
def print_recipe_details(recipe_id, name, category, tags, nutrition):
    print(f"ID: {recipe_id}, Name: {name}, Category: {category}")
    print(f"Tags: {', '.join(tags)}")
    print(f"Nutrition: Calories: {nutrition['calories']}, Protein: {nutrition['protein']}g, Carbs: {nutrition['carbs']}g, Fat: {nutrition['fat']}g")
    print("-" * 80)

# Get all recipes with their nutrition information
cursor.execute("""
    SELECT r.id, r.name, r.category, r.tags, 
           n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
    FROM recipes r
    JOIN nutrition n ON r.id = n.recipe_id
    ORDER BY r.id
""")

recipes = cursor.fetchall()

# Count recipes by type and health goals
veg_count = 0
non_veg_count = 0
weight_loss_count = 0
weight_gain_count = 0
diabetic_count = 0
energy_boost_count = 0
protein_rich_count = 0

# Print all recipes
print("\n===== ALL RECIPES =====\n")
for recipe in recipes:
    recipe_id, name, category, tags_json, calories, protein, carbs, fat, fiber, sugar, sodium = recipe
    tags = json.loads(tags_json)
    
    # Count by type
    if "vegetarian" in tags:
        veg_count += 1
    if "non_vegetarian" in tags:
        non_veg_count += 1
    
    # Count by health goal
    if "weight_loss" in tags:
        weight_loss_count += 1
    if "weight_gain" in tags:
        weight_gain_count += 1
    if "diabetic" in tags:
        diabetic_count += 1
    if "energy_boost" in tags:
        energy_boost_count += 1
    if "protein" in tags:
        protein_rich_count += 1
    
    # Create nutrition dictionary
    nutrition = {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "fiber": fiber,
        "sugar": sugar,
        "sodium": sodium
    }
    
    print_recipe_details(recipe_id, name, category, tags, nutrition)

# Print summary
print("\n===== RECIPE SUMMARY =====\n")
print(f"Total Recipes: {len(recipes)}")
print(f"Vegetarian Recipes: {veg_count}")
print(f"Non-Vegetarian Recipes: {non_veg_count}")
print(f"Weight Loss Recipes: {weight_loss_count}")
print(f"Weight Gain Recipes: {weight_gain_count}")
print(f"Diabetic-Friendly Recipes: {diabetic_count}")
print(f"Energy Boost Recipes: {energy_boost_count}")
print(f"Protein-Rich Recipes: {protein_rich_count}")

# Print recipes by meal type
print("\n===== RECIPES BY MEAL TYPE =====\n")
meal_types = ["breakfast", "lunch", "dinner", "snack", "main_course", "side_dish"]

for meal_type in meal_types:
    cursor.execute("""
        SELECT COUNT(*) FROM recipes WHERE category = ?
    """, (meal_type,))
    count = cursor.fetchone()[0]
    print(f"{meal_type.capitalize()}: {count} recipes")

# Close connection
conn.close()