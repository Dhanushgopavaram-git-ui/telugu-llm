import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# New vegetarian recipes with appropriate tags
veg_recipes = [
    {
        "name": "Tomato Pappu",
        "category": "main_course",
        "ingredients": ["toor dal", "tomatoes", "onions", "green chilies", "turmeric", "salt", "mustard seeds", "cumin seeds", "curry leaves"],
        "instructions": "1. Cook toor dal until soft. 2. In a pan, add oil and temper with mustard seeds, cumin, and curry leaves. 3. Add chopped onions and green chilies, sauté until golden. 4. Add chopped tomatoes and cook until soft. 5. Add cooked dal, turmeric, salt and simmer for 5-7 minutes.",
        "cooking_time": 30,
        "tags": ["vegetarian", "healthy", "protein", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 220,
            "protein": 12,
            "carbs": 30,
            "fat": 5,
            "fiber": 8,
            "sugar": 4,
            "sodium": 400
        }
    },
    {
        "name": "Avakaya Pachadi",
        "category": "side_dish",
        "ingredients": ["raw mango", "red chili powder", "mustard powder", "salt", "sesame oil", "fenugreek powder", "turmeric"],
        "instructions": "1. Cut raw mangoes into small pieces. 2. Mix all spices together. 3. Add oil and mix well. 4. Add mango pieces and mix thoroughly. 5. Store in an airtight container for at least 3 days before consuming.",
        "cooking_time": 40,
        "tags": ["vegetarian", "traditional", "spicy", "pickle"],
        "nutrition": {
            "calories": 180,
            "protein": 2,
            "carbs": 15,
            "fat": 12,
            "fiber": 3,
            "sugar": 10,
            "sodium": 800
        }
    },
    {
        "name": "Bendakaya Pulusu",
        "category": "main_course",
        "ingredients": ["okra", "tamarind paste", "jaggery", "turmeric", "salt", "mustard seeds", "cumin seeds", "curry leaves", "red chili powder"],
        "instructions": "1. Cut okra into pieces. 2. In a pan, add oil and temper with mustard seeds, cumin, and curry leaves. 3. Add okra and sauté until slightly soft. 4. Add tamarind paste, jaggery, turmeric, salt, and red chili powder. 5. Add water and simmer for 15 minutes.",
        "cooking_time": 30,
        "tags": ["vegetarian", "healthy", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 150,
            "protein": 4,
            "carbs": 20,
            "fat": 7,
            "fiber": 6,
            "sugar": 8,
            "sodium": 350
        }
    },
    {
        "name": "Pesara Garelu",
        "category": "breakfast",
        "ingredients": ["moong dal", "rice flour", "onions", "green chilies", "ginger", "cumin seeds", "salt"],
        "instructions": "1. Soak moong dal for 2 hours and grind to a coarse paste. 2. Add rice flour, chopped onions, green chilies, ginger, cumin seeds, and salt. 3. Mix well to form a thick batter. 4. Heat oil in a pan and drop spoonfuls of batter to form small patties. 5. Fry until golden brown on both sides.",
        "cooking_time": 25,
        "tags": ["vegetarian", "protein", "breakfast", "energy_boost"],
        "nutrition": {
            "calories": 280,
            "protein": 14,
            "carbs": 35,
            "fat": 10,
            "fiber": 5,
            "sugar": 2,
            "sodium": 300
        }
    },
    {
        "name": "Ragi Sangati",
        "category": "main_course",
        "ingredients": ["ragi flour", "rice", "water", "salt"],
        "instructions": "1. Cook rice until soft. 2. In a separate pan, add water and bring to a boil. 3. Add ragi flour slowly, stirring continuously to avoid lumps. 4. Add cooked rice and salt. 5. Mix well and cook for 5 more minutes.",
        "cooking_time": 30,
        "tags": ["vegetarian", "healthy", "weight_loss", "diabetic", "energy_boost"],
        "nutrition": {
            "calories": 200,
            "protein": 6,
            "carbs": 40,
            "fat": 1,
            "fiber": 7,
            "sugar": 0,
            "sodium": 200
        }
    }
]

# New non-vegetarian recipes with appropriate tags
non_veg_recipes = [
    {
        "name": "Andhra Chicken Curry",
        "category": "main_course",
        "ingredients": ["chicken", "onions", "tomatoes", "ginger-garlic paste", "red chili powder", "turmeric", "coriander powder", "garam masala", "curry leaves", "oil", "salt"],
        "instructions": "1. Marinate chicken with turmeric, salt, and red chili powder. 2. In a pan, heat oil and add chopped onions. 3. Sauté until golden brown. 4. Add ginger-garlic paste and cook for 2 minutes. 5. Add tomatoes and cook until soft. 6. Add all spices and cook for 2 minutes. 7. Add chicken and cook until tender. 8. Garnish with curry leaves.",
        "cooking_time": 45,
        "tags": ["non_vegetarian", "spicy", "protein", "weight_gain", "energy_boost"],
        "nutrition": {
            "calories": 350,
            "protein": 30,
            "carbs": 10,
            "fat": 20,
            "fiber": 2,
            "sugar": 3,
            "sodium": 600
        }
    },
    {
        "name": "Fish Pulusu",
        "category": "main_course",
        "ingredients": ["fish", "tamarind paste", "onions", "tomatoes", "turmeric", "red chili powder", "coriander powder", "mustard seeds", "curry leaves", "oil", "salt"],
        "instructions": "1. Clean and cut fish into pieces. 2. In a pan, heat oil and add mustard seeds and curry leaves. 3. Add chopped onions and sauté until golden. 4. Add tomatoes and cook until soft. 5. Add all spices and cook for 2 minutes. 6. Add tamarind paste and water. 7. Add fish pieces and cook until done.",
        "cooking_time": 35,
        "tags": ["non_vegetarian", "spicy", "protein", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 250,
            "protein": 25,
            "carbs": 8,
            "fat": 12,
            "fiber": 2,
            "sugar": 4,
            "sodium": 500
        }
    },
    {
        "name": "Natu Kodi Pulusu",
        "category": "main_course",
        "ingredients": ["country chicken", "onions", "tomatoes", "ginger-garlic paste", "red chili powder", "turmeric", "coriander powder", "curry leaves", "oil", "salt"],
        "instructions": "1. Clean and cut chicken into pieces. 2. In a pan, heat oil and add curry leaves. 3. Add chopped onions and sauté until golden. 4. Add ginger-garlic paste and cook for 2 minutes. 5. Add tomatoes and cook until soft. 6. Add all spices and cook for 2 minutes. 7. Add chicken and cook until tender.",
        "cooking_time": 50,
        "tags": ["non_vegetarian", "spicy", "protein", "traditional", "energy_boost"],
        "nutrition": {
            "calories": 320,
            "protein": 28,
            "carbs": 12,
            "fat": 18,
            "fiber": 3,
            "sugar": 5,
            "sodium": 550
        }
    },
    {
        "name": "Mutton Curry",
        "category": "main_course",
        "ingredients": ["mutton", "onions", "tomatoes", "ginger-garlic paste", "red chili powder", "turmeric", "coriander powder", "garam masala", "curry leaves", "oil", "salt"],
        "instructions": "1. Clean and cut mutton into pieces. 2. In a pressure cooker, heat oil and add chopped onions. 3. Sauté until golden brown. 4. Add ginger-garlic paste and cook for 2 minutes. 5. Add tomatoes and cook until soft. 6. Add all spices and cook for 2 minutes. 7. Add mutton and pressure cook until tender.",
        "cooking_time": 60,
        "tags": ["non_vegetarian", "spicy", "protein", "weight_gain", "energy_boost"],
        "nutrition": {
            "calories": 380,
            "protein": 32,
            "carbs": 10,
            "fat": 22,
            "fiber": 2,
            "sugar": 3,
            "sodium": 650
        }
    },
    {
        "name": "Prawn Masala",
        "category": "main_course",
        "ingredients": ["prawns", "onions", "tomatoes", "ginger-garlic paste", "red chili powder", "turmeric", "coriander powder", "curry leaves", "oil", "salt"],
        "instructions": "1. Clean prawns and marinate with turmeric and salt. 2. In a pan, heat oil and add curry leaves. 3. Add chopped onions and sauté until golden. 4. Add ginger-garlic paste and cook for 2 minutes. 5. Add tomatoes and cook until soft. 6. Add all spices and cook for 2 minutes. 7. Add prawns and cook until done.",
        "cooking_time": 30,
        "tags": ["non_vegetarian", "spicy", "protein", "weight_loss", "diabetic"],
        "nutrition": {
            "calories": 280,
            "protein": 26,
            "carbs": 8,
            "fat": 15,
            "fiber": 2,
            "sugar": 3,
            "sodium": 600
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

# Add all vegetarian recipes
print("Adding vegetarian recipes...")
for recipe in veg_recipes:
    recipe_id = add_recipe(recipe)
    print(f"Added {recipe['name']} with ID {recipe_id}")

# Add all non-vegetarian recipes
print("\nAdding non-vegetarian recipes...")
for recipe in non_veg_recipes:
    recipe_id = add_recipe(recipe)
    print(f"Added {recipe['name']} with ID {recipe_id}")

# Commit changes and close connection
conn.commit()
conn.close()

print("\nAll recipes added successfully!")