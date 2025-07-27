import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# Get all recipes with their categories
cursor.execute("""
    SELECT id, name, category, tags
    FROM recipes
    ORDER BY id
""")

recipes = cursor.fetchall()

# Count recipes by category
category_counts = {}
for recipe in recipes:
    recipe_id, name, category, tags_json = recipe
    
    if category not in category_counts:
        category_counts[category] = 0
    category_counts[category] += 1

# Print all recipes with their categories
print("\n===== RECIPES WITH CATEGORIES =====\n")
for recipe in recipes:
    recipe_id, name, category, tags_json = recipe
    tags = json.loads(tags_json)
    
    print(f"ID: {recipe_id}, Name: {name}")
    print(f"Category: {category}")
    print(f"Tags: {', '.join(tags)}")
    print("-" * 80)

# Print category counts
print("\n===== CATEGORY COUNTS =====\n")
for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{category}: {count} recipes")

# Close connection
conn.close()