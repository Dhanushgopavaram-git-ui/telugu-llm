import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# New breakfast, lunch, and dinner recipes
more_recipes = [
    # Breakfast recipes
    {
        "name": "Attu with Peanut Chutney",
        "category": "breakfast",
        "ingredients": ["rice flour", "onions", "green chilies", "cumin seeds", "peanuts", "red chilies", "garlic", "salt", "oil"],
        "instructions": "1. Mix rice flour with water to make a thin batter. 2. Add chopped onions, green chilies, cumin seeds, and salt. 3. Heat a pan and pour the batter to make a thin pancake. 4. Cook until crispy on both sides. 5. For chutney, roast peanuts, red chilies, and garlic. 6. Grind with salt and water to make a smooth paste.",
        "cooking_time": 20,
        "tags": ["vegetarian", "breakfast", "quick", "weight_loss"],
        "nutrition": {
            "calories": 220,
            "protein": 7,
            "carbs": 30,
            "fat": 8,
            "fiber": 4,
            "sugar": 2,
            "sodium": 300
        }
    },
    {
        "name": "Egg Dosa",
        "category": "breakfast",
        "ingredients": ["dosa batter", "eggs", "onions", "green chilies", "coriander leaves", "salt", "oil"],
        "instructions": "1. Pour dosa batter on a hot pan to make a thin pancake. 2. Beat eggs with chopped onions, green chilies, coriander leaves, and salt. 3. Pour the egg mixture on top of the dosa. 4. Cook until the egg is set and the dosa is crispy.",
        "cooking_time": 15,
        "tags": ["non_vegetarian", "breakfast", "protein", "weight_gain"],
        "nutrition": {
            "calories": 280,
            "protein": 15,
            "carbs": 30,
            "fat": 12,
            "fiber": 2,
            "sugar": 1,
            "sodium": 350
        }
    },
    
    # Lunch recipes
    {
        "name": "Pulihora Rice",
        "category": "lunch",
        "ingredients": ["rice", "tamarind paste", "peanuts", "mustard seeds", "cumin seeds", "turmeric", "curry leaves", "green chilies", "salt", "oil"],
        "instructions": "1. Cook rice and let it cool. 2. In a pan, heat oil and add mustard seeds, cumin seeds, and curry leaves. 3. Add peanuts and roast until golden. 4. Add green chilies, turmeric, and tamarind paste. 5. Mix well and add salt. 6. Add cooked rice and mix thoroughly.",
        "cooking_time": 30,
        "tags": ["vegetarian", "lunch", "traditional", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 320,
            "protein": 8,
            "carbs": 55,
            "fat": 9,
            "fiber": 5,
            "sugar": 3,
            "sodium": 400
        }
    },
    {
        "name": "Andhra Chicken Biryani",
        "category": "lunch",
        "ingredients": ["basmati rice", "chicken", "onions", "tomatoes", "ginger-garlic paste", "biryani masala", "green chilies", "mint leaves", "coriander leaves", "yogurt", "oil", "salt"],
        "instructions": "1. Marinate chicken with yogurt, ginger-garlic paste, biryani masala, and salt. 2. Cook rice until 70% done. 3. In a pan, heat oil and add chopped onions. 4. Sauté until golden brown. 5. Add marinated chicken and cook until tender. 6. Layer partially cooked rice over chicken. 7. Garnish with mint and coriander leaves. 8. Cover and cook on low heat for 20 minutes.",
        "cooking_time": 60,
        "tags": ["non_vegetarian", "lunch", "spicy", "protein", "weight_gain", "energy_boost"],
        "nutrition": {
            "calories": 450,
            "protein": 30,
            "carbs": 50,
            "fat": 15,
            "fiber": 3,
            "sugar": 2,
            "sodium": 600
        }
    },
    {
        "name": "Vegetable Pulao",
        "category": "lunch",
        "ingredients": ["basmati rice", "mixed vegetables", "onions", "ginger-garlic paste", "green chilies", "cumin seeds", "bay leaf", "cinnamon", "cloves", "cardamom", "oil", "salt"],
        "instructions": "1. Soak rice for 30 minutes. 2. In a pan, heat oil and add whole spices. 3. Add chopped onions and sauté until golden. 4. Add ginger-garlic paste and green chilies. 5. Add mixed vegetables and cook for 5 minutes. 6. Add soaked rice and water. 7. Cook until rice is done.",
        "cooking_time": 40,
        "tags": ["vegetarian", "lunch", "healthy", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 350,
            "protein": 7,
            "carbs": 60,
            "fat": 8,
            "fiber": 6,
            "sugar": 4,
            "sodium": 350
        }
    },
    
    # Dinner recipes
    {
        "name": "Chapati with Palak Paneer",
        "category": "dinner",
        "ingredients": ["wheat flour", "spinach", "paneer", "onions", "tomatoes", "ginger-garlic paste", "green chilies", "garam masala", "cumin powder", "oil", "salt"],
        "instructions": "1. Make chapati dough with wheat flour, water, and salt. 2. Roll into thin circles and cook on a hot pan. 3. For palak paneer, blanch spinach and blend to a smooth paste. 4. In a pan, heat oil and add chopped onions. 5. Add ginger-garlic paste and green chilies. 6. Add tomatoes and cook until soft. 7. Add spinach paste and spices. 8. Add paneer cubes and cook for 5 minutes.",
        "cooking_time": 45,
        "tags": ["vegetarian", "dinner", "healthy", "protein", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 380,
            "protein": 18,
            "carbs": 45,
            "fat": 14,
            "fiber": 8,
            "sugar": 5,
            "sodium": 450
        }
    },
    {
        "name": "Fish Curry with Rice",
        "category": "dinner",
        "ingredients": ["fish", "rice", "onions", "tomatoes", "ginger-garlic paste", "green chilies", "turmeric", "red chili powder", "coriander powder", "curry leaves", "oil", "salt"],
        "instructions": "1. Clean and cut fish into pieces. 2. Cook rice until done. 3. In a pan, heat oil and add curry leaves. 4. Add chopped onions and sauté until golden. 5. Add ginger-garlic paste and green chilies. 6. Add tomatoes and cook until soft. 7. Add all spices and cook for 2 minutes. 8. Add fish pieces and cook until done. 9. Serve with rice.",
        "cooking_time": 40,
        "tags": ["non_vegetarian", "dinner", "protein", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 420,
            "protein": 28,
            "carbs": 50,
            "fat": 10,
            "fiber": 3,
            "sugar": 4,
            "sodium": 500
        }
    },
    {
        "name": "Ragi Roti with Peanut Chutney",
        "category": "dinner",
        "ingredients": ["ragi flour", "onions", "green chilies", "coriander leaves", "peanuts", "red chilies", "garlic", "salt", "oil"],
        "instructions": "1. Mix ragi flour with chopped onions, green chilies, coriander leaves, and salt. 2. Add water to make a soft dough. 3. Roll into thin circles and cook on a hot pan. 4. For chutney, roast peanuts, red chilies, and garlic. 5. Grind with salt and water to make a smooth paste.",
        "cooking_time": 30,
        "tags": ["vegetarian", "dinner", "healthy", "weight_loss", "diabetic", "energy_boost"],
        "nutrition": {
            "calories": 280,
            "protein": 10,
            "carbs": 40,
            "fat": 9,
            "fiber": 7,
            "sugar": 2,
            "sodium": 350
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

# Add all recipes
print("Adding more recipes with specific meal types...")
for recipe in more_recipes:
    recipe_id = add_recipe(recipe)
    print(f"Added {recipe['name']} with ID {recipe_id}")

# Commit changes and close connection
conn.commit()
conn.close()

print("\nAll additional recipes added successfully!")