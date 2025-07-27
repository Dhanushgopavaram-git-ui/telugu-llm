import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# New snack recipes
snack_recipes = [
    {
        "name": "Masala Vada",
        "category": "snack",
        "ingredients": ["chana dal", "onions", "green chilies", "ginger", "curry leaves", "coriander leaves", "salt", "oil"],
        "instructions": "1. Soak chana dal for 2 hours and grind to a coarse paste. 2. Add chopped onions, green chilies, ginger, curry leaves, coriander leaves, and salt. 3. Mix well to form a thick batter. 4. Heat oil in a pan and drop spoonfuls of batter to form small patties. 5. Fry until golden brown on both sides.",
        "cooking_time": 30,
        "tags": ["vegetarian", "snack", "protein", "energy_boost"],
        "nutrition": {
            "calories": 250,
            "protein": 12,
            "carbs": 30,
            "fat": 10,
            "fiber": 6,
            "sugar": 2,
            "sodium": 350
        }
    },
    {
        "name": "Mirchi Bajji",
        "category": "snack",
        "ingredients": ["green chilies", "gram flour", "rice flour", "red chili powder", "turmeric", "salt", "oil"],
        "instructions": "1. Slit green chilies lengthwise and remove seeds. 2. Mix gram flour, rice flour, red chili powder, turmeric, and salt with water to form a thick batter. 3. Dip green chilies in the batter and deep fry until golden brown.",
        "cooking_time": 20,
        "tags": ["vegetarian", "snack", "spicy", "traditional"],
        "nutrition": {
            "calories": 180,
            "protein": 5,
            "carbs": 20,
            "fat": 10,
            "fiber": 3,
            "sugar": 1,
            "sodium": 300
        }
    },
    {
        "name": "Punugulu",
        "category": "snack",
        "ingredients": ["dosa batter", "onions", "green chilies", "coriander leaves", "cumin seeds", "salt", "oil"],
        "instructions": "1. Take leftover dosa batter or fermented rice and urad dal batter. 2. Add chopped onions, green chilies, coriander leaves, cumin seeds, and salt. 3. Mix well. 4. Heat oil in a pan and drop spoonfuls of batter. 5. Fry until golden brown on all sides.",
        "cooking_time": 25,
        "tags": ["vegetarian", "snack", "traditional", "weight_loss"],
        "nutrition": {
            "calories": 200,
            "protein": 6,
            "carbs": 25,
            "fat": 9,
            "fiber": 2,
            "sugar": 1,
            "sodium": 320
        }
    },
    {
        "name": "Chicken 65",
        "category": "snack",
        "ingredients": ["chicken", "yogurt", "ginger-garlic paste", "red chili powder", "turmeric", "garam masala", "corn flour", "egg", "salt", "oil"],
        "instructions": "1. Cut chicken into small pieces. 2. Marinate with yogurt, ginger-garlic paste, red chili powder, turmeric, garam masala, corn flour, egg, and salt for 2 hours. 3. Deep fry until golden brown and crispy.",
        "cooking_time": 40,
        "tags": ["non_vegetarian", "snack", "spicy", "protein", "energy_boost"],
        "nutrition": {
            "calories": 320,
            "protein": 25,
            "carbs": 10,
            "fat": 18,
            "fiber": 1,
            "sugar": 2,
            "sodium": 550
        }
    },
    {
        "name": "Sabudana Vada",
        "category": "snack",
        "ingredients": ["sabudana", "potatoes", "peanuts", "green chilies", "cumin seeds", "coriander leaves", "salt", "oil"],
        "instructions": "1. Soak sabudana for 2 hours. 2. Boil and mash potatoes. 3. Roast and crush peanuts. 4. Mix sabudana, potatoes, peanuts, chopped green chilies, cumin seeds, coriander leaves, and salt. 5. Form into small patties and deep fry until golden brown.",
        "cooking_time": 35,
        "tags": ["vegetarian", "snack", "energy_boost", "weight_gain"],
        "nutrition": {
            "calories": 280,
            "protein": 7,
            "carbs": 40,
            "fat": 12,
            "fiber": 3,
            "sugar": 1,
            "sodium": 330
        }
    }
]

# Function to add a recipe to the database
def add_recipe(recipe):
    # Insert into recipes table
    cursor.execute(
        "INSERT INTO recipes (name, category, ingredients, instructions, cooking_time, tags) VALUES (?, ?, ?, ?, ?, ?)",
        (recipe['name'], recipe['category'], json.dumps(recipe['ingredients']), recipe['instructions'], recipe['cooking_time'], json.dumps(recipe['tags']))
    )
    
    # Get the ID of the inserted recipe
    recipe_id = cursor.lastrowid
    
    # Insert into nutrition table
    cursor.execute(
        "INSERT INTO nutrition (recipe_id, calories, protein, carbs, fat, fiber, sugar, sodium) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (recipe_id, recipe['nutrition']['calories'], recipe['nutrition']['protein'], recipe['nutrition']['carbs'], 
         recipe['nutrition']['fat'], recipe['nutrition']['fiber'], recipe['nutrition']['sugar'], recipe['nutrition']['sodium'])
    )
    
    return recipe_id

# Add all snack recipes
print("Adding snack recipes...")
for recipe in snack_recipes:
    recipe_id = add_recipe(recipe)
    print(f"Added {recipe['name']} with ID {recipe_id}")

# Commit changes and close connection
conn.commit()
conn.close()

print("\nAll snack recipes added successfully!")