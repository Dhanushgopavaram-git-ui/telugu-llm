import json
import random
from datetime import datetime, timedelta
from database import RecipeDatabase
from nutrition_api import NutritionAPI

class TeluguDietGenerator:
    def __init__(self):
        self.db = RecipeDatabase()
        self.nutrition_api = NutritionAPI()
        
        # Telugu diet categories and meal types
        self.meal_types = {
            'breakfast': 'అల్పాహారం',
            'lunch': 'మధ్యాహ్న భోజనం',
            'dinner': 'రాత్రి భోజనం',
            'snack': 'చిరుతిండి'
        }
        
        # Diet preferences in Telugu
        self.diet_preferences = {
            'vegetarian': 'శాకాహారం',
            'non_vegetarian': 'మాంసాహారం',
            'vegan': 'శుద్ధ శాకాహారం',
            'diabetic': 'మధుమేహం',
            'weight_loss': 'బరువు తగ్గించడం',
            'weight_gain': 'బరువు పెంచడం',
            'protein_rich': 'ప్రోటీన్ ధన్యం',
            'low_carb': 'తక్కువ కార్బోహైడ్రేట్',
            'high_fiber': 'ఎక్కువ ఫైబర్',
            'energy_boost': 'శక్తి పెంపు',
            'immunity': 'రోగనిరోధక శక్తి'
        }
        
        # Telugu health goals
        self.health_goals = {
            'energy_boost': 'శక్తి పెంపు',
            'immunity': 'రోగనిరోధక శక్తి',
            'digestion': 'జీర్ణక్రియ',
            'heart_health': 'గుండె ఆరోగ్యం',
            'bone_health': 'ఎముకల ఆరోగ్యం',
            'brain_health': 'మెదడు ఆరోగ్యం'
        }
    
    def generate_diet_menu(self, user_input):
        """
        Generate a personalized Telugu diet menu based on user input
        """
        try:
            # Parse user input
            preferences = self._parse_user_input(user_input)
            
            # Get available recipes
            all_recipes = self.db.get_all_recipes()
            
            # Filter recipes based on preferences
            filtered_recipes = self._filter_recipes(all_recipes, preferences)
            
            # Generate meal plan
            meal_plan = self._create_meal_plan(filtered_recipes, preferences)
            
            # Calculate nutrition summary
            nutrition_summary = self._calculate_nutrition_summary(meal_plan)
            
            # Generate Telugu recommendations
            recommendations = self._generate_telugu_recommendations(preferences)
            
            return {
                'meal_plan': meal_plan,
                'nutrition_summary': nutrition_summary,
                'recommendations': recommendations,
                'preferences': preferences
            }
            
        except Exception as e:
            return {
                'error': f'ఆహార పట్టిక తయారీ విఫలమైంది: {str(e)}',
                'meal_plan': {},
                'nutrition_summary': {},
                'recommendations': []
            }
    
    def _parse_user_input(self, user_input):
        """Parse user input to extract preferences"""
        preferences = {
            'diet_type': 'vegetarian',
            'health_goal': 'energy_boost',
            'calorie_target': 2000,
            'meals_per_day': 3,
            'allergies': [],
            'dislikes': [],
            'duration': 7  # days
        }
        
        # Extract diet type
        if any(word in user_input.lower() for word in ['non-veg', 'non veg', 'meat', 'chicken']):
            preferences['diet_type'] = 'non_vegetarian'
        elif any(word in user_input.lower() for word in ['vegan', 'strict vegetarian']):
            preferences['diet_type'] = 'vegan'
        
        # Extract health goals
        if any(word in user_input.lower() for word in ['diabetic', 'diabetes', 'sugar']):
            preferences['health_goal'] = 'diabetic'
        elif any(word in user_input.lower() for word in ['weight loss', 'lose weight', 'slim']):
            preferences['health_goal'] = 'weight_loss'
        elif any(word in user_input.lower() for word in ['weight gain', 'gain weight', 'bulk']):
            preferences['health_goal'] = 'weight_gain'
        elif any(word in user_input.lower() for word in ['protein', 'muscle']):
            preferences['health_goal'] = 'protein_rich'
        
        # Extract calorie target
        if 'calorie' in user_input.lower():
            import re
            calorie_match = re.search(r'(\d+)\s*calorie', user_input.lower())
            if calorie_match:
                preferences['calorie_target'] = int(calorie_match.group(1))
        
        # Extract duration
        if 'week' in user_input.lower():
            preferences['duration'] = 7
        elif 'month' in user_input.lower():
            preferences['duration'] = 30
        
        return preferences
    
    def _filter_recipes(self, recipes, preferences):
        """Filter recipes based on user preferences"""
        filtered = []
        
        # First pass: filter by diet type
        diet_filtered = []
        for recipe in recipes:
            # Check diet type using tags
            if preferences['diet_type'] == 'vegetarian':
                if 'non_vegetarian' in recipe.get('tags', []):
                    continue
            elif preferences['diet_type'] == 'vegan':
                if any(tag in recipe.get('tags', []) for tag in ['non_vegetarian', 'dairy']):
                    continue
            diet_filtered.append(recipe)
        
        # If no recipes match diet type, use all recipes
        if not diet_filtered:
            diet_filtered = recipes
        
        # Second pass: filter by health goal
        health_goal_filtered = []
        
        # Try to find recipes that match health goal
        for recipe in diet_filtered:
            match = False
            
            # Check health goals using tags and nutrition
            if preferences['health_goal'] == 'diabetic':
                # Low sugar recipes
                sugar = recipe['nutrition'].get('sugar', 0)
                if sugar is not None and sugar <= 10:  # Low sugar content
                    match = True
            elif preferences['health_goal'] == 'weight_loss':
                # Low calorie recipes
                calories = recipe['nutrition'].get('calories', 0)
                if calories is not None and calories <= 300:  # Low calorie
                    match = True
                # Or recipes with healthy tag
                if 'healthy' in recipe.get('tags', []):
                    match = True
            elif preferences['health_goal'] == 'weight_gain':
                # High calorie recipes
                calories = recipe['nutrition'].get('calories', 0)
                if calories is not None and calories >= 500:  # High calorie
                    match = True
            elif preferences['health_goal'] == 'energy_boost' or preferences['health_goal'] == 'protein_rich':
                # High protein recipes
                protein = recipe['nutrition'].get('protein', 0)
                if protein is not None and protein >= 10:  # High protein
                    match = True
                # Or recipes with protein tag
                if 'protein' in recipe.get('tags', []):
                    match = True
            
            if match:
                health_goal_filtered.append(recipe)
        
        # If no recipes match health goal, use diet filtered recipes
        if not health_goal_filtered:
            health_goal_filtered = diet_filtered
        
        # Third pass: filter by meal type preferences
        for recipe in health_goal_filtered:
            # Check for allergies
            if preferences['allergies']:
                ingredients_text = ' '.join(recipe.get('ingredients', [])).lower()
                if any(allergy.lower() in ingredients_text for allergy in preferences['allergies']):
                    continue
            
            filtered.append(recipe)
        
        # If no recipes match after all filtering, use original recipes
        if not filtered:
            filtered = recipes
        
        # Ensure we have enough variety by using all recipes if filtered set is too small
        if len(filtered) < 5:
            filtered = recipes
        
        return filtered
        
        return filtered
    
    def _create_meal_plan(self, recipes, preferences):
        """Create a meal plan for the specified duration"""
        meal_plan = {}
        
        # Make a copy of recipes to avoid modifying the original list
        available_recipes = recipes.copy()
        
        for day in range(1, preferences['duration'] + 1):
            date = datetime.now() + timedelta(days=day-1)
            day_key = date.strftime('%Y-%m-%d')
            
            # Set a different seed for each day to ensure variety
            day_seed = f"{preferences['diet_type']}_{preferences['health_goal']}_{day}"
            day_seed_val = sum(ord(c) for c in day_seed)
            random.seed(day_seed_val)
            
            meal_plan[day_key] = {
                'day': day,
                'date': date.strftime('%A, %B %d'),
                'telugu_date': self._get_telugu_date(date),
                'meals': {}
            }
            
            # Track selected recipes for this day to avoid duplicates
            selected_recipes_ids = set()
            
            # Generate meals for the day
            if preferences['meals_per_day'] >= 3:
                for meal_type in ['breakfast', 'lunch', 'dinner']:
                    meal = self._select_meal(recipes, meal_type, preferences)
                    
                    # Try to avoid duplicates within the same day if we have enough recipes
                    if meal and len(recipes) > preferences['meals_per_day']:
                        attempts = 0
                        while meal.get('id') in selected_recipes_ids and attempts < 3:
                            meal = self._select_meal(recipes, meal_type, preferences)
                            attempts += 1
                    
                    meal_plan[day_key]['meals'][meal_type] = meal
                    if meal:
                        selected_recipes_ids.add(meal.get('id'))
            
            if preferences['meals_per_day'] >= 4:
                snack = self._select_meal(recipes, 'snack', preferences)
                
                # Try to avoid duplicates if possible
                if snack and len(recipes) > preferences['meals_per_day']:
                    attempts = 0
                    while snack.get('id') in selected_recipes_ids and attempts < 3:
                        snack = self._select_meal(recipes, 'snack', preferences)
                        attempts += 1
                
                meal_plan[day_key]['meals']['snack'] = snack
                if snack:
                    selected_recipes_ids.add(snack.get('id'))
            
            # Reset random seed after each day
            random.seed()
        
        return meal_plan
    
    
    def _select_meal(self, recipes, meal_type, preferences):
        """Select appropriate recipe for a meal type"""
        import random
        
        # Set a different seed based on preferences to ensure different menus for different conditions
        seed_str = f"{preferences['diet_type']}_{preferences['health_goal']}_{meal_type}"
        seed_val = sum(ord(c) for c in seed_str)
        random.seed(seed_val)
        
        suitable_recipes = []
        
        # First try to find recipes that match the meal type category exactly
        primary_matches = []
        for recipe in recipes:
            # Handle both dictionary and integer recipe representations
            if isinstance(recipe, int):
                # If recipe is just an ID, fetch the full recipe from the database
                recipe_obj = self.db.get_recipe(recipe)
                if recipe_obj and recipe_obj.get('category') == meal_type:
                    primary_matches.append(recipe_obj)
            elif isinstance(recipe, dict):
                if recipe.get('category') == meal_type:
                    primary_matches.append(recipe)
        
        # If we have primary matches, prioritize those
        if primary_matches:
            suitable_recipes.extend(primary_matches)
        else:
            # Otherwise use broader criteria
            for recipe in recipes:
                # Handle both dictionary and integer recipe representations
                recipe_obj = recipe
                if isinstance(recipe, int):
                    recipe_obj = self.db.get_recipe(recipe)
                    if not recipe_obj:
                        continue
                
                if meal_type == 'breakfast':
                    if (recipe_obj.get('category') == 'breakfast' or 
                        'breakfast' in recipe_obj.get('tags', []) or
                        (recipe_obj.get('cooking_time', 0) <= 20)):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'lunch':
                    if (recipe_obj.get('category') == 'main_course' or
                        recipe_obj.get('category') == 'lunch' or
                        recipe_obj.get('nutrition', {}).get('calories', 0) >= 300):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'dinner':
                    if (recipe_obj.get('category') == 'main_course' or
                        recipe_obj.get('category') == 'dinner' or
                        recipe_obj.get('nutrition', {}).get('calories', 0) <= 400):
                        suitable_recipes.append(recipe_obj)
                
                elif meal_type == 'snack':
                    if (recipe_obj.get('category') == 'snack' or
                        'snack' in recipe_obj.get('tags', []) or
                        recipe_obj.get('nutrition', {}).get('calories', 0) <= 200):
                        suitable_recipes.append(recipe_obj)
        
        # If we have suitable recipes, choose one randomly
        if suitable_recipes:
            selected = random.choice(suitable_recipes)
        else:
            # Fallback to any recipe
            if recipes:
                if isinstance(recipes[0], int):
                    recipe_id = random.choice(recipes)
                    selected = self.db.get_recipe(recipe_id)
                else:
                    selected = random.choice(recipes)
            else:
                selected = None
        
        # Reset the random seed to avoid affecting other randomizations
        random.seed()
        
        return selected
    def _calculate_nutrition_summary(self, meal_plan):
        """Calculate total nutrition for the meal plan"""
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'sodium': 0
        }
        
        meal_count = 0
        
        for day_data in meal_plan.values():
            for meal in day_data['meals'].values():
                if meal and meal.get('nutrition'):
                    for key in total_nutrition:
                        if key in meal['nutrition'] and meal['nutrition'][key] is not None:
                            total_nutrition[key] += meal['nutrition'][key]
                    meal_count += 1
        
        # Calculate averages
        if meal_count > 0:
            for key in total_nutrition:
                total_nutrition[key] = round(total_nutrition[key] / meal_count, 1)
        
        return total_nutrition
    
    def _generate_telugu_recommendations(self, preferences):
        """Generate Telugu recommendations based on preferences"""
        recommendations = []
        
        # Diet type recommendations
        if preferences['diet_type'] == 'vegetarian':
            recommendations.append("శాకాహార ఆహారం తీసుకోవడం వల్ల హృదయ ఆరోగ్యం మెరుగవుతుంది")
            recommendations.append("ప్రతి రోజు కూరగాయలు మరియు పండ్లు తీసుకోవాలి")
            recommendations.append("పప్పులు మరియు బీన్స్ తీసుకోవడం వల్ల ప్రోటీన్ లభిస్తుంది")
        
        elif preferences['diet_type'] == 'vegan':
            recommendations.append("శుద్ధ శాకాహార ఆహారం తీసుకోవడం వల్ల ఆరోగ్యం మెరుగవుతుంది")
            recommendations.append("బాదం పప్పు మరియు సోయా ఉత్పత్తులు తీసుకోవాలి")
        
        elif preferences['health_goal'] == 'diabetic':
            recommendations.append("చక్కెర మరియు కార్బోహైడ్రేట్ తక్కువగా తీసుకోవాలి")
            recommendations.append("ఫైబర్ ఎక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
            recommendations.append("మెత్తని ఆహారం తీసుకోవాలి")
        
        elif preferences['health_goal'] == 'weight_loss':
            recommendations.append("కేలరీలు తక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
            recommendations.append("నీరు ఎక్కువగా తాగాలి")
            recommendations.append("వ్యాయామం చేయడం మర్చిపోవద్దు")
        
        elif preferences['health_goal'] == 'protein_rich':
            recommendations.append("ప్రోటీన్ ఎక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
            recommendations.append("బీన్స్ మరియు పప్పులు తీసుకోవాలి")
            recommendations.append("అండ్లు మరియు చేపలు తీసుకోవాలి")
        
        elif preferences['health_goal'] == 'energy_boost':
            recommendations.append("ఎక్కువ కేలరీలు ఉన్న ఆహారం తీసుకోవాలి")
            recommendations.append("విటమిన్లు మరియు ఖనిజాలు ఎక్కువగా తీసుకోవాలి")
            recommendations.append("పండ్లు మరియు కూరగాయలు తీసుకోవాలి")
        
        # General recommendations
        recommendations.append("ప్రతి రోజు 8 గంటల నిద్ర తీసుకోవాలి")
        recommendations.append("వ్యాయామం చేయడం మర్చిపోవద్దు")
        recommendations.append("ఆహారాన్ని నెమ్మదిగా మరియు బాగా నమలాలి")
        recommendations.append("ప్రతి రోజు 8-10 గ్లాస్ నీరు తాగాలి")
        recommendations.append("ఆహారాన్ని సమయానికి తీసుకోవాలి")
        
        return recommendations
    
    def _get_telugu_date(self, date):
        """Convert date to Telugu format"""
        telugu_months = {
            1: 'జనవరి', 2: 'ఫిబ్రవరి', 3: 'మార్చి', 4: 'ఏప్రిల్',
            5: 'మే', 6: 'జూన్', 7: 'జూలై', 8: 'ఆగస్టు',
            9: 'సెప్టెంబర్', 10: 'అక్టోబర్', 11: 'నవంబర్', 12: 'డిసెంబర్'
        }
        
        telugu_days = {
            'Monday': 'సోమవారం', 'Tuesday': 'మంగళవారం', 'Wednesday': 'బుధవారం',
            'Thursday': 'గురువారం', 'Friday': 'శుక్రవారం', 'Saturday': 'శనివారం', 'Sunday': 'ఆదివారం'
        }
        
        day_name = date.strftime('%A')
        month = date.month
        day = date.day
        
        return f"{telugu_days[day_name]}, {telugu_months[month]} {day}"
    
    def get_diet_suggestions(self, user_input):
        """Get diet suggestions based on user input"""
        suggestions = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': []
        }
        
        # Parse user input for meal preferences
        if 'breakfast' in user_input.lower() or 'అల్పాహారం' in user_input:
            suggestions['breakfast'] = [
                'ఇడ్లీ సాంబార్',
                'దోసా చట్నీ',
                'పొంగల్',
                'ఉప్మా',
                'పూరి కూర'
            ]
        
        if 'lunch' in user_input.lower() or 'మధ్యాహ్న' in user_input:
            suggestions['lunch'] = [
                'పులిహోర',
                'బిర్యానీ',
                'కూర',
                'రసం',
                'పప్పు'
            ]
        
        if 'dinner' in user_input.lower() or 'రాత్రి' in user_input:
            suggestions['dinner'] = [
                'రోటీ కూర',
                'ఖిచ్డీ',
                'సాంబార్ రైస్',
                'దాల్ రైస్'
            ]
        
        return suggestions