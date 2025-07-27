import json
import sqlite3
from diet_generator import TeluguDietGenerator
from database import RecipeDatabase
from nutrition_api import NutritionAPI

# Initialize components
diet_generator = TeluguDietGenerator()
# Access the database and nutrition API from the diet generator
db = diet_generator.db
nutrition_api = diet_generator.nutrition_api

# Test function to verify recipe ID handling
def test_recipe_id_handling():
    print("Testing recipe ID handling in diet generator...\n")
    
    # Get all recipes from the database
    from config import DATABASE_PATH
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.id, r.name, r.category 
        FROM recipes r
        JOIN nutrition n ON r.id = n.recipe_id
        LIMIT 5
    """)
    
    recipes = cursor.fetchall()
    print(f"Sample recipes from database:")
    for recipe in recipes:
        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Category: {recipe[2]}")
    
    print("\nTesting _select_meal method with recipe IDs...")
    
    # Create a list of recipe IDs
    recipe_ids = [recipe[0] for recipe in recipes]
    
    # Test preferences
    preferences = {
        'diet_type': 'vegetarian',
        'health_goal': 'weight_loss'
    }
    
    # Test meal types
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    
    for meal_type in meal_types:
        selected_recipe = diet_generator._select_meal(recipe_ids, meal_type, preferences)
        if selected_recipe:
            print(f"For {meal_type}, selected: ID: {selected_recipe.get('id')}, "
                  f"Name: {selected_recipe.get('name')}, "
                  f"Category: {selected_recipe.get('category')}")
        else:
            print(f"No recipe selected for {meal_type}")
    
    # Test generating a full diet menu
    print("\nGenerating a full diet menu...")
    menu = diet_generator.generate_diet_menu("vegetarian diet for weight loss")
    
    # Check if menu was generated successfully
    if menu and 'daily_plans' in menu:
        print(f"Successfully generated menu with {len(menu['daily_plans'])} days")
        
        # Check the first day's meals
        if menu['daily_plans']:
            first_day = menu['daily_plans'][0]
            print(f"\nFirst day meals:")
            for meal in first_day['meals']:
                print(f"Meal type: {meal['meal_type']}, "
                      f"Recipe: {meal['recipe']['name']}, "
                      f"Category: {meal['recipe']['category']}")
    else:
        print("Failed to generate menu")
    
    conn.close()

# Run the test
if __name__ == "__main__":
    test_recipe_id_handling()