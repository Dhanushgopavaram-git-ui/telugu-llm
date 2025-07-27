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

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# RAG System Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gpt-3.5-turbo"