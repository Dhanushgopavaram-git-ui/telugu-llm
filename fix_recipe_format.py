import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# Function to get recipe details with nutrition
def get_recipe_with_nutrition(recipe_id):
    cursor.execute(r"""
        SELECT r.id, r.name, r.category, r.ingredients, r.instructions, r.cooking_time, r.tags,
               n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
        FROM recipes r
        JOIN nutrition n ON r.id = n.recipe_id
        WHERE r.id = ?
    """, (recipe_id,))
    
    row = cursor.fetchone()
    if not row:
        return None
    
    recipe_id, name, category, ingredients_json, instructions, cooking_time, tags_json, \
    calories, protein, carbs, fat, fiber, sugar, sodium = row
    
    return {
        'id': recipe_id,
        'name': name,
        'category': category,
        'ingredients': json.loads(ingredients_json),
        'instructions': instructions,
        'cooking_time': cooking_time,
        'tags': json.loads(tags_json),
        'nutrition': {
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'fiber': fiber,
            'sugar': sugar,
            'sodium': sodium
        }
    }

# Function to update the _select_meal method in diet_generator.py
def update_select_meal_method():
    try:
        with open('diet_generator.py', 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        with open('diet_generator.py', 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Find the _select_meal method
    start_marker = "def _select_meal(self, recipes, meal_type, preferences):"
    end_marker = "def _calculate_nutrition_summary"
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        print("Could not find _select_meal method in diet_generator.py")
        return False
    
    # Extract the method
    method_content = content[start_index:end_index]
    
    # Check if the method already handles recipe IDs
    if "isinstance(recipe, int)" in method_content:
        print("Method already handles recipe IDs")
        return False
    
    # Update the method to handle recipe IDs
    updated_method = """
    def _select_meal(self, recipes, meal_type, preferences):
        \"\"\"Select appropriate recipe for a meal type\"\"\"
        import random
        
        # Set a different seed based on preferences to ensure different menus for different conditions
        seed_str = f"{preferences['diet_type']}_{preferences['health_goal']}_{meal_type}"
        seed_val = sum(ord(c) for c in seed_str)
        random.seed(seed_val)
        
        suitable_recipes = []
        
        # First try to find recipes that match the meal type category exactly
        primary_matches = []
        for recipe in recipes:
            # Handle both dictionary and integer recipe representations
            if isinstance(recipe, int):
                # If recipe is just an ID, fetch the full recipe from the database
                recipe_obj = self.db.get_recipe(recipe)
                if recipe_obj and recipe_obj.get('category') == meal_type:
                    primary_matches.append(recipe_obj)
            elif isinstance(recipe, dict):
                if recipe.get('category') == meal_type:
                    primary_matches.append(recipe)
        
        # If we have primary matches, prioritize those
        if primary_matches:
            suitable_recipes.extend(primary_matches)
        else:
            # Otherwise use broader criteria
            for recipe in recipes:
                # Handle both dictionary and integer recipe representations
                recipe_obj = recipe
                if isinstance(recipe, int):
                    recipe_obj = self.db.get_recipe(recipe)
                    if not recipe_obj:
                        continue
                
                if meal_type == 'breakfast':
                    if (recipe_obj.get('category') == 'breakfast' or 
                        'breakfast' in recipe_obj.get('tags', []) or
                        (recipe_obj.get('cooking_time', 0) <= 20)):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'lunch':
                    if (recipe_obj.get('category') == 'main_course' or
                        recipe_obj.get('category') == 'lunch' or
                        recipe_obj.get('nutrition', {}).get('calories', 0) >= 300):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'dinner':
                    if (recipe_obj.get('category') == 'main_course' or
                        recipe_obj.get('category') == 'dinner' or
                        recipe_obj.get('nutrition', {}).get('calories', 0) <= 400):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'snack':
                    if (recipe_obj.get('category') == 'snack' or
                        'snack' in recipe_obj.get('tags', []) or
                        recipe_obj.get('nutrition', {}).get('calories', 0) <= 200):
                        suitable_recipes.append(recipe_obj)
        
        # If we have suitable recipes, choose one randomly
        if suitable_recipes:
            selected = random.choice(suitable_recipes)
        else:
            # Fallback to any recipe
            if recipes:
                if isinstance(recipes[0], int):
                    recipe_id = random.choice(recipes)
                    selected = self.db.get_recipe(recipe_id)
                else:
                    selected = random.choice(recipes)
            else:
                selected = None
        
        # Reset the random seed to avoid affecting other randomizations
        random.seed()
        
        return selected
    """
    
    # Replace the method in the content
    new_content = content[:start_index] + updated_method + content[end_index:]
    
    # Write the updated content back to the file
    with open('diet_generator.py', 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print("Updated _select_meal method in diet_generator.py")
    return True

# Function to update the database class to handle recipe IDs
def update_database_class():
    try:
        with open('database.py', 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with a different encoding
        with open('database.py', 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Check if the get_recipe method already exists
    if "def get_recipe(self, recipe_id):" in content:
        print("get_recipe method already exists in database.py")
        return False
    
    # Find the class definition
    class_marker = "class RecipeDatabase:"
    
    class_index = content.find(class_marker)
    
    if class_index == -1:
        print("Could not find RecipeDatabase class in database.py")
        return False
    
    # Find a good place to insert the new method
    method_marker = "def get_all_recipes(self):"
    
    method_index = content.find(method_marker, class_index)
    
    if method_index == -1:
        print("Could not find a good place to insert the new method in database.py")
        return False
    
    # Find the end of the method
    next_method_index = content.find("def ", method_index + len(method_marker))
    
    if next_method_index == -1:
        next_method_index = len(content)
    
    # Insert the new method
    new_method = """
    def get_recipe(self, recipe_id):
        \"\"\"Get a single recipe by ID with nutrition information\"\"\"
        try:
            self.cursor.execute(\"\"\"
                SELECT r.id, r.name, r.category, r.ingredients, r.instructions, r.cooking_time, r.tags,
                       n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
                FROM recipes r
                JOIN nutrition n ON r.id = n.recipe_id
                WHERE r.id = ?
            \"\"\", (recipe_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            recipe_id, name, category, ingredients_json, instructions, cooking_time, tags_json, \
            calories, protein, carbs, fat, fiber, sugar, sodium = row
            
            return {
                'id': recipe_id,
                'name': name,
                'category': category,
                'ingredients': json.loads(ingredients_json),
                'instructions': instructions,
                'cooking_time': cooking_time,
                'tags': json.loads(tags_json),
                'nutrition': {
                    'calories': calories,
                    'protein': protein,
                    'carbs': carbs,
                    'fat': fat,
                    'fiber': fiber,
                    'sugar': sugar,
                    'sodium': sodium
                }
            }
        except Exception as e:
            print(f"Error getting recipe: {e}")
            return None
    """
    
    # Insert the new method after the get_all_recipes method
    new_content = content[:next_method_index] + new_method + content[next_method_index:]
    
    # Write the updated content back to the file
    with open('database.py', 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print("Added get_recipe method to database.py")
    return True

# Main execution
print("Fixing recipe format issues...")

# Update the database class
db_updated = update_database_class()

# Update the _select_meal method
method_updated = update_select_meal_method()

if db_updated or method_updated:
    print("\nUpdates completed successfully!")
    print("The diet generator should now handle recipe IDs correctly.")
    print("Please restart the Streamlit app to apply the changes.")
else:
    print("\nNo updates were needed.")

# Close connection
conn.close()