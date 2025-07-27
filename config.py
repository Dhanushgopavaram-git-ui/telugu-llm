import os
from dotenv import load_dotenv

load_dotenv()

# Nutrition API Configuration
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY', '')
NUTRITION_API_URL = "https://api.edamam.com/api/nutrition-data"

# Database Configuration
DATABASE_PATH = "telugu_recipes.db"

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
FLASK_DEBUG = True 