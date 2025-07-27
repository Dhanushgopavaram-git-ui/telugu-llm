import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# Get recipe count
cursor.execute('SELECT COUNT(*) FROM recipes')
print(f'Number of recipes: {cursor.fetchone()[0]}')

# Get recipe categories
cursor.execute('SELECT DISTINCT category FROM recipes')
categories = [row[0] for row in cursor.fetchall()]
print(f'Categories: {categories}')

# Get recipe tags
cursor.execute('SELECT DISTINCT tags FROM recipes')
tags = [row[0] for row in cursor.fetchall()]
print(f'Tags: {tags[:5]}')

# Get recipe details
cursor.execute('SELECT id, name, category, tags FROM recipes')
print('\nRecipes:')
for row in cursor.fetchall():
    print(f'ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Tags: {row[3]}')

# Check if there are any non-vegetarian recipes
cursor.execute("SELECT COUNT(*) FROM recipes WHERE tags LIKE '%non_vegetarian%'")
non_veg_count = cursor.fetchone()[0]
print(f'\nNon-vegetarian recipes: {non_veg_count}')

# Check recipes by health goal
health_goals = ['weight_loss', 'weight_gain', 'diabetic', 'energy_boost']
for goal in health_goals:
    cursor.execute(f"SELECT COUNT(*) FROM recipes WHERE tags LIKE '%{goal}%'")
    count = cursor.fetchone()[0]
    print(f'Recipes for {goal}: {count}')

conn.close()