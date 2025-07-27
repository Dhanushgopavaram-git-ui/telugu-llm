from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import RecipeDatabase
from nutrition_api import NutritionAPI
from recipe_processor import RecipeProcessor
from diet_generator import TeluguDietGenerator
from config import FLASK_SECRET_KEY, FLASK_DEBUG
import json

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.debug = FLASK_DEBUG

# Initialize components
db = RecipeDatabase()
nutrition_api = NutritionAPI()
processor = RecipeProcessor()
diet_generator = TeluguDietGenerator()

@app.route('/')
def index():
    """Main page with search and recipe display"""
    recipes = db.get_all_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/search')
def search():
    """Search recipes"""
    query = request.args.get('q', '')
    if query:
        recipes = db.search_recipes(query)
    else:
        recipes = db.get_all_recipes()
    return render_template('search_results.html', recipes=recipes, query=query)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Show detailed recipe information"""
    recipes = db.get_all_recipes()
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return redirect(url_for('index'))

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """Add a new recipe"""
    if request.method == 'POST':
        data = request.get_json()
        
        recipe_id = db.add_recipe(
            name=data['name'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            cooking_time=data.get('cooking_time'),
            difficulty=data.get('difficulty', 'Medium')
        )
        
        # Get nutrition data
        nutrition_data = nutrition_api.get_nutrition_data(data['ingredients'])
        db.add_nutrition(recipe_id, nutrition_data)
        
        return jsonify({'success': True, 'recipe_id': recipe_id})
    
    return render_template('add_recipe.html')

@app.route('/api/recipes')
def api_recipes():
    """API endpoint to get all recipes"""
    recipes = db.get_all_recipes()
    return jsonify(recipes)

@app.route('/api/search')
def api_search():
    """API endpoint to search recipes"""
    query = request.args.get('q', '')
    if query:
        recipes = db.search_recipes(query)
    else:
        recipes = db.get_all_recipes()
    return jsonify(recipes)

@app.route('/api/categories')
def api_categories():
    """API endpoint to get all categories"""
    categories = db.get_categories()
    return jsonify(categories)

@app.route('/api/tags')
def api_tags():
    """API endpoint to get all tags"""
    tags = db.get_tags()
    return jsonify(tags)

@app.route('/api/recipes/category/<category>')
def api_recipes_by_category(category):
    """API endpoint to get recipes by category"""
    recipes = db.get_recipes_by_category(category)
    return jsonify(recipes)

@app.route('/api/recipes/tags')
def api_recipes_by_tags():
    """API endpoint to get recipes by tags"""
    tags = request.args.getlist('tags')
    recipes = db.get_recipes_by_tags(tags)
    return jsonify(recipes)

@app.route('/advanced_search')
def advanced_search():
    """Advanced search page"""
    return render_template('advanced_search.html')

@app.route('/api/advanced_search')
def api_advanced_search():
    """API endpoint for advanced search with multiple filters"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    max_time = request.args.get('max_time', '')
    tags = request.args.getlist('tags')
    
    # Get all recipes first
    recipes = db.get_all_recipes()
    filtered_recipes = []
    
    for recipe in recipes:
        # Filter by query
        if query and query.lower() not in recipe['name'].lower():
            continue
            
        # Filter by category
        if category and recipe.get('category') != category:
            continue
            
        # Filter by difficulty
        if difficulty and recipe.get('difficulty') != difficulty:
            continue
            
        # Filter by cooking time
        if max_time and recipe.get('cooking_time', 0) > int(max_time):
            continue
            
        # Filter by tags
        if tags:
            recipe_tags = recipe.get('tags', [])
            if not any(tag in recipe_tags for tag in tags):
                continue
        
        filtered_recipes.append(recipe)
    
    return jsonify(filtered_recipes)

@app.route('/initialize')
def initialize():
    """Initialize the database with sample recipes"""
    processor.process_pulihora_recipes()
    return redirect(url_for('index'))

@app.route('/initialize_all')
def initialize_all():
    """Initialize the database with all Telugu recipes"""
    processor.process_all_telugu_recipes()
    return redirect(url_for('index'))

@app.route('/diet_menu', methods=['GET', 'POST'])
def diet_menu():
    """Generate personalized diet menu"""
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        diet_plan = diet_generator.generate_diet_menu(user_input)
        return render_template('diet_menu.html', diet_plan=diet_plan, user_input=user_input)
    
    return render_template('diet_menu.html')

@app.route('/api/generate_diet', methods=['POST'])
def api_generate_diet():
    """API endpoint to generate diet menu"""
    data = request.get_json()
    user_input = data.get('user_input', '')
    
    diet_plan = diet_generator.generate_diet_menu(user_input)
    return jsonify(diet_plan)

@app.route('/diet_suggestions')
def diet_suggestions():
    """Get diet suggestions based on user input"""
    query = request.args.get('q', '')
    suggestions = diet_generator.get_diet_suggestions(query)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 