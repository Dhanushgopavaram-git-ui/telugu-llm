import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class RecipeDatabase:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create recipes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                cooking_time INTEGER,
                difficulty TEXT,
                category TEXT DEFAULT 'main_course',
                cuisine_type TEXT DEFAULT 'Telugu',
                tags TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create nutrition table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nutrition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                calories REAL,
                protein REAL,
                carbs REAL,
                fat REAL,
                fiber REAL,
                sugar REAL,
                sodium REAL,
                nutrition_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_recipe(self, name, ingredients, instructions, cooking_time=None, difficulty=None, category='main_course', cuisine_type='Telugu', tags=None):
        """Add a new recipe to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if tags is None:
            tags = []
        
        cursor.execute('''
            INSERT INTO recipes (name, ingredients, instructions, cooking_time, difficulty, category, cuisine_type, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, json.dumps(ingredients), instructions, cooking_time, difficulty, category, cuisine_type, json.dumps(tags)))
        
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id
    
    def add_nutrition(self, recipe_id, nutrition_data):
        """Add nutrition information for a recipe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO nutrition (recipe_id, calories, protein, carbs, fat, fiber, sugar, sodium, nutrition_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe_id,
            nutrition_data.get('calories', 0),
            nutrition_data.get('protein', 0),
            nutrition_data.get('carbs', 0),
            nutrition_data.get('fat', 0),
            nutrition_data.get('fiber', 0),
            nutrition_data.get('sugar', 0),
            nutrition_data.get('sodium', 0),
            json.dumps(nutrition_data)
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_recipes(self):
        """Get all recipes with nutrition data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
            FROM recipes r
            LEFT JOIN nutrition n ON r.id = n.recipe_id
            ORDER BY r.name
        ''')
        
        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'ingredients': json.loads(row[2]),
                'instructions': row[3],
                'cooking_time': row[4],
                'difficulty': row[5],
                'category': row[6],
                'cuisine_type': row[7],
                'tags': json.loads(row[8]) if row[8] else [],
                'created_at': row[9],
                'nutrition': {
                    'calories': row[11],
                    'protein': row[12],
                    'carbs': row[13],
                    'fat': row[14],
                    'fiber': row[15],
                    'sugar': row[16],
                    'sodium': row[17]
                }
            }
            recipes.append(recipe)
        
        conn.close()
        return recipes
    
    
    def get_recipe(self, recipe_id):
        """Get a single recipe by ID with nutrition information"""
        try:
            self.cursor.execute("""
                SELECT r.id, r.name, r.category, r.ingredients, r.instructions, r.cooking_time, r.tags,
                       n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
                FROM recipes r
                JOIN nutrition n ON r.id = n.recipe_id
                WHERE r.id = ?
            """, (recipe_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            recipe_id, name, category, ingredients_json, instructions, cooking_time, tags_json,             calories, protein, carbs, fat, fiber, sugar, sodium = row
            
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
    def get_recipes_by_category(self, category):
        """Get recipes by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
            FROM recipes r
            LEFT JOIN nutrition n ON r.id = n.recipe_id
            WHERE r.category = ?
            ORDER BY r.name
        ''', (category,))
        
        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'ingredients': json.loads(row[2]),
                'instructions': row[3],
                'cooking_time': row[4],
                'difficulty': row[5],
                'category': row[6],
                'cuisine_type': row[7],
                'tags': json.loads(row[8]) if row[8] else [],
                'created_at': row[9],
                'nutrition': {
                    'calories': row[11],
                    'protein': row[12],
                    'carbs': row[13],
                    'fat': row[14],
                    'fiber': row[15],
                    'sugar': row[16],
                    'sodium': row[17]
                }
            }
            recipes.append(recipe)
        
        conn.close()
        return recipes
    
    def get_recipes_by_tags(self, tags):
        """Get recipes by tags"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert tags list to JSON string for LIKE search
        tag_conditions = []
        for tag in tags:
            tag_conditions.append(f"r.tags LIKE '%{tag}%'")
        
        where_clause = " OR ".join(tag_conditions) if tag_conditions else "1=1"
        
        cursor.execute(f'''
            SELECT r.*, n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
            FROM recipes r
            LEFT JOIN nutrition n ON r.id = n.recipe_id
            WHERE {where_clause}
            ORDER BY r.name
        ''')
        
        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'ingredients': json.loads(row[2]),
                'instructions': row[3],
                'cooking_time': row[4],
                'difficulty': row[5],
                'category': row[6],
                'cuisine_type': row[7],
                'tags': json.loads(row[8]) if row[8] else [],
                'created_at': row[9],
                'nutrition': {
                    'calories': row[11],
                    'protein': row[12],
                    'carbs': row[13],
                    'fat': row[14],
                    'fiber': row[15],
                    'sugar': row[16],
                    'sodium': row[17]
                }
            }
            recipes.append(recipe)
        
        conn.close()
        return recipes
    
    def get_categories(self):
        """Get all available categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT category FROM recipes ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return categories
    
    def get_tags(self):
        """Get all available tags"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT tags FROM recipes WHERE tags IS NOT NULL')
        all_tags = set()
        for row in cursor.fetchall():
            if row[0]:
                tags = json.loads(row[0])
                all_tags.update(tags)
        
        conn.close()
        return sorted(list(all_tags))
    
    def search_recipes(self, query):
        """Search recipes by name or ingredients"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, n.calories, n.protein, n.carbs, n.fat, n.fiber, n.sugar, n.sodium
            FROM recipes r
            LEFT JOIN nutrition n ON r.id = n.recipe_id
            WHERE r.name LIKE ? OR r.ingredients LIKE ?
            ORDER BY r.name
        ''', (f'%{query}%', f'%{query}%'))
        
        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'ingredients': json.loads(row[2]),
                'instructions': row[3],
                'cooking_time': row[4],
                'difficulty': row[5],
                'category': row[6],
                'cuisine_type': row[7],
                'tags': json.loads(row[8]) if row[8] else [],
                'created_at': row[9],
                'nutrition': {
                    'calories': row[11],
                    'protein': row[12],
                    'carbs': row[13],
                    'fat': row[14],
                    'fiber': row[15],
                    'sugar': row[16],
                    'sodium': row[17]
                }
            }
            recipes.append(recipe)
        
        conn.close()
        return recipes 
    
    def get_recipe(self, recipe_id):
        """Get a single recipe by ID with nutrition information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
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
            
            recipe = {
                'id': recipe_id,
                'name': name,
                'category': category,
                'ingredients': json.loads(ingredients_json),
                'instructions': instructions,
                'cooking_time': cooking_time,
                'tags': json.loads(tags_json) if tags_json else [],
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
            
            conn.close()
            return recipe
        except Exception as e:
            print(f"Error getting recipe: {e}")
            return None