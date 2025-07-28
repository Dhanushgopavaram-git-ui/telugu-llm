import sqlite3

DB_PATH = "veg_diet_recipes.db"

def create_veg_recipe_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veg_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Dish TEXT,
            Ingredients TEXT,
            Calories INTEGER,
            Protein_g INTEGER,
            Carbs_g INTEGER,
            Fat_g INTEGER,
            Fiber_g INTEGER,
            Preparation TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_veg_recipe_table()
    print("veg_recipes table created in veg_diet_recipes.db")
