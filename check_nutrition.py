import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('telugu_recipes.db')
cursor = conn.cursor()

# Get nutrition information
cursor.execute('SELECT recipe_id, calories, protein, carbs, fat, sugar FROM nutrition')
print('Nutrition information:')
for row in cursor.fetchall():
    print(f'Recipe ID: {row[0]}, Calories: {row[1]}, Protein: {row[2]}g, Carbs: {row[3]}g, Fat: {row[4]}g, Sugar: {row[5]}g')

# Check recipes with high calories (>400)
cursor.execute('SELECT COUNT(*) FROM nutrition WHERE calories > 400')
high_calorie_count = cursor.fetchone()[0]
print(f'\nHigh calorie recipes (>400): {high_calorie_count}')

# Check recipes with low calories (<300)
cursor.execute('SELECT COUNT(*) FROM nutrition WHERE calories < 300')
low_calorie_count = cursor.fetchone()[0]
print(f'Low calorie recipes (<300): {low_calorie_count}')

# Check recipes with high protein (>10g)
cursor.execute('SELECT COUNT(*) FROM nutrition WHERE protein > 10')
high_protein_count = cursor.fetchone()[0]
print(f'High protein recipes (>10g): {high_protein_count}')

# Check recipes with high sugar (>20g)
cursor.execute('SELECT COUNT(*) FROM nutrition WHERE sugar > 20')
high_sugar_count = cursor.fetchone()[0]
print(f'High sugar recipes (>20g): {high_sugar_count}')

conn.close()