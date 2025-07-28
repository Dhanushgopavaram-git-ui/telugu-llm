import json
import random
import os
from datetime import datetime, timedelta
from database import RecipeDatabase
from nutrition_api import NutritionAPI

class TeluguDietGenerator:
    def __init__(self):
        """Initialize the Telugu Diet Generator with non-vegetarian focus only"""
        # Initialize database connection
        self.db = RecipeDatabase()
        
        # Remove any vegetarian recipe references
        self.recipes = []  # Will be loaded from CSV
        
        # Diet preferences in Telugu - only non-vegetarian
        self.diet_preferences = {
            'non_vegetarian': 'మాంసాహారం',
            'diabetic': 'మధుమేహం',
            'weight_loss': 'బరువు తగ్గించడం',
            'weight_gain': 'బరువు పెంచడం',
            'protein_rich': 'ప్రోటీన్ ధన్యం',
            'low_carb': 'తక్కువ కార్బోహైడ్రేట్',
            'high_fiber': 'ఎక్కువ ఫైబర్',
            'energy_boost': 'శక్తి పెంపు',
            'immunity': 'రోగనిరోధక శక్తి'
        }
        
        # Meal types in Telugu
        self.meal_types = {
            'breakfast': 'అల్పాహారం',
            'lunch': 'మధ్యాహ్న భోజనం',
            'dinner': 'రాత్రి భోజనం',
            'snack': 'చిరుతిండి'
        }
        
        # Health conditions and their dietary requirements
        self.health_conditions = {
            'diabetic': {
                'avoid': ['high_sugar', 'refined_carbs'],
                'prefer': ['low_glycemic', 'high_fiber', 'protein_rich']
            },
            'weight_loss': {
                'avoid': ['high_calorie', 'fried'],
                'prefer': ['low_calorie', 'high_protein', 'high_fiber']
            },
            'weight_gain': {
                'avoid': ['very_low_calorie'],
                'prefer': ['high_calorie', 'protein_rich', 'healthy_fats']
            }
        }
    
    def _load_non_veg_recipes(self):
        """Load non-vegetarian recipes from CSV file"""
        recipes = []
        csv_file = os.path.join(os.path.dirname(__file__), 'non_veg_diet_recipes.csv')

        try:
            import pandas as pd
            # Use pandas to properly handle multi-line CSV entries with proper quoting
            df = pd.read_csv(csv_file, quotechar='"', skipinitialspace=True, encoding='utf-8')

            for index, row in df.iterrows():
                try:
                    recipe_name = str(row['Dish']).strip()
                    ingredients = str(row['Ingredients (with quantities)']).strip()
                    calories = int(row['Calories']) if pd.notna(row['Calories']) else 0
                    protein = int(row['Protein_g']) if pd.notna(row['Protein_g']) else 0
                    carbs = int(row['Carbs_g']) if pd.notna(row['Carbs_g']) else 0
                    fat = int(row['Fat_g']) if pd.notna(row['Fat_g']) else 0
                    fiber = int(row['Fiber_g']) if pd.notna(row['Fiber_g']) else 0
                    instructions = str(row['Preparation']).strip() if pd.notna(row['Preparation']) else "Cook as directed"

                    recipe = {
                        'id': f'nonveg_{index + 1}',
                        'name': recipe_name,
                        'ingredients': [ing.strip() for ing in ingredients.split(',')],
                        'instructions': instructions,
                        'preparation': instructions,  # Add preparation field for Streamlit compatibility
                        'nutrition': {
                            'calories': calories,
                            'protein': protein,
                            'carbs': carbs,
                            'fat': fat,
                            'fiber': fiber
                        },
                        'category': 'non_vegetarian',
                        'tags': ['non_vegetarian'],
                        'cooking_time': 30  # Default cooking time
                    }

                    recipes.append(recipe)

                except Exception as e:
                    print(f"Error parsing row {index}: {e}")
                    continue

            print(f"Successfully loaded {len(recipes)} non-vegetarian recipes from CSV")

        except ImportError:
            print("pandas not available, using fallback CSV parsing")
            recipes = self._load_csv_fallback(csv_file)
        except FileNotFoundError:
            print(f"CSV file not found: {csv_file}")
            print("Using sample non-vegetarian recipes as fallback")
            recipes = self._create_sample_nonveg_recipes()
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            recipes = self._create_sample_nonveg_recipes()

        return recipes

    def _load_veg_recipes(self):
        """Load vegetarian recipes from CSV file"""
        recipes = []
        csv_file = os.path.join(os.path.dirname(__file__), 'veg_diet_recipes.csv')

        try:
            import pandas as pd
            # Use pandas to properly handle multi-line CSV entries with proper quoting
            df = pd.read_csv(csv_file, quotechar='"', skipinitialspace=True, encoding='utf-8')

            for index, row in df.iterrows():
                try:
                    recipe_name = str(row['Dish']).strip()
                    ingredients = str(row['Ingredients']).strip()  # Note: different column name for veg recipes

                    # Parse nutrition information
                    calories = int(row['Calories']) if pd.notna(row['Calories']) else 300
                    protein = float(row['Protein_g']) if pd.notna(row['Protein_g']) else 10
                    carbs = float(row['Carbs_g']) if pd.notna(row['Carbs_g']) else 40
                    fat = float(row['Fat_g']) if pd.notna(row['Fat_g']) else 10
                    fiber = float(row['Fiber_g']) if pd.notna(row['Fiber_g']) else 5

                    # Get preparation instructions
                    preparation = str(row['Preparation']).strip() if pd.notna(row['Preparation']) else "Cook as directed"

                    # Create recipe object
                    recipe = {
                        'id': f'veg_{index}',
                        'name': recipe_name,
                        'ingredients': ingredients.split(',') if ',' in ingredients else [ingredients],
                        'nutrition': {
                            'calories': calories,
                            'protein': protein,
                            'carbs': carbs,
                            'fat': fat,
                            'fiber': fiber
                        },
                        'instructions': preparation,
                        'preparation': preparation,  # For compatibility
                        'category': 'vegetarian',
                        'tags': ['vegetarian'],
                        'cooking_time': 30
                    }

                    recipes.append(recipe)

                except Exception as e:
                    print(f"Error parsing vegetarian row {index}: {e}")
                    continue

            print(f"Successfully loaded {len(recipes)} vegetarian recipes from CSV")

        except ImportError:
            print("pandas not available, using fallback CSV parsing for vegetarian recipes")
            recipes = self._load_veg_csv_fallback(csv_file)
        except FileNotFoundError:
            print(f"Vegetarian CSV file not found: {csv_file}")
            print("Using sample vegetarian recipes as fallback")
            recipes = self._create_sample_veg_recipes()
        except Exception as e:
            print(f"Error loading vegetarian CSV file: {e}")
            recipes = self._create_sample_veg_recipes()

        return recipes

    def _load_csv_fallback(self, csv_file):
        """Fallback CSV parsing without pandas"""
        recipes = []
        try:
            import csv
            with open(csv_file, 'r', encoding='utf-8') as file:
                # Read the entire file content first
                content = file.read()

                # Split by lines but handle multi-line entries
                lines = content.split('\n')
                current_row = []
                in_quotes = False

                for line in lines[1:]:  # Skip header
                    if not line.strip():
                        continue

                    # Simple parsing - look for complete rows
                    if line.count(',') >= 6 and not in_quotes:
                        if current_row:
                            # Process previous row
                            self._process_csv_row(current_row, recipes, len(recipes) + 1)
                        current_row = [line]
                    else:
                        if current_row:
                            current_row.append(line)

                # Process last row
                if current_row:
                    self._process_csv_row(current_row, recipes, len(recipes) + 1)

        except Exception as e:
            print(f"Fallback CSV parsing failed: {e}")
            return self._create_sample_nonveg_recipes()

        return recipes

    def _load_veg_csv_fallback(self, csv_file):
        """Fallback CSV parsing for vegetarian recipes without pandas"""
        recipes = []
        try:
            import csv
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for index, row in enumerate(reader):
                    try:
                        recipe = {
                            'id': f'veg_{index}',
                            'name': row['Dish'].strip(),
                            'ingredients': row['Ingredients'].split(','),
                            'nutrition': {
                                'calories': int(row['Calories']) if row['Calories'] else 300,
                                'protein': float(row['Protein_g']) if row['Protein_g'] else 10,
                                'carbs': float(row['Carbs_g']) if row['Carbs_g'] else 40,
                                'fat': float(row['Fat_g']) if row['Fat_g'] else 10,
                                'fiber': float(row['Fiber_g']) if row['Fiber_g'] else 5
                            },
                            'instructions': row['Preparation'].strip() if row['Preparation'] else "Cook as directed",
                            'preparation': row['Preparation'].strip() if row['Preparation'] else "Cook as directed",
                            'category': 'vegetarian',
                            'tags': ['vegetarian'],
                            'cooking_time': 30
                        }
                        recipes.append(recipe)
                    except Exception as e:
                        print(f"Error parsing vegetarian fallback row {index}: {e}")
                        continue
        except Exception as e:
            print(f"Vegetarian fallback CSV parsing failed: {e}")
            return self._create_sample_veg_recipes()

        return recipes

    def _create_sample_veg_recipes(self):
        """Create sample vegetarian recipes as fallback"""
        return [
            {
                'id': 'veg_khichdi',
                'name': 'Vegetable Khichdi',
                'ingredients': ['1/2 cup rice', '1/4 cup moong dal', '1 cup mixed vegetables', 'spices'],
                'nutrition': {'calories': 320, 'protein': 11, 'carbs': 48, 'fat': 8, 'fiber': 6},
                'instructions': 'Cook rice and dal with vegetables and spices until soft',
                'preparation': 'Cook rice and dal with vegetables and spices until soft',
                'category': 'vegetarian',
                'tags': ['vegetarian'],
                'cooking_time': 30
            },
            {
                'id': 'veg_palak_paneer',
                'name': 'Palak Paneer',
                'ingredients': ['200g spinach', '100g paneer', '1 onion', 'spices'],
                'nutrition': {'calories': 280, 'protein': 14, 'carbs': 12, 'fat': 20, 'fiber': 5},
                'instructions': 'Cook spinach with paneer and spices',
                'preparation': 'Cook spinach with paneer and spices',
                'category': 'vegetarian',
                'tags': ['vegetarian'],
                'cooking_time': 25
            },
            {
                'id': 'veg_chickpea_salad',
                'name': 'Chickpea Salad',
                'ingredients': ['1 cup chickpeas', '1 cucumber', '1 tomato', 'lemon juice'],
                'nutrition': {'calories': 250, 'protein': 12, 'carbs': 35, 'fat': 8, 'fiber': 10},
                'instructions': 'Mix chickpeas with vegetables and dressing',
                'preparation': 'Mix chickpeas with vegetables and dressing',
                'category': 'vegetarian',
                'tags': ['vegetarian'],
                'cooking_time': 15
            }
        ]

    def _process_csv_row(self, row_lines, recipes, recipe_id):
        """Process a CSV row that might span multiple lines"""
        try:
            # Join all lines and try to parse
            full_line = ' '.join(row_lines).strip()

            # Simple regex-based parsing for the specific CSV format
            import re

            # Pattern to match: Name,"ingredients",calories,protein,carbs,fat,fiber,"instructions"
            pattern = r'^([^,]+),"([^"]+)",(\d+),(\d+),(\d+),(\d+),(\d+),"(.+)"$'
            match = re.match(pattern, full_line, re.DOTALL)

            if match:
                recipe_name = match.group(1).strip()
                ingredients = match.group(2).strip()
                calories = int(match.group(3))
                protein = int(match.group(4))
                carbs = int(match.group(5))
                fat = int(match.group(6))
                fiber = int(match.group(7))
                instructions = match.group(8).strip()

                recipe = {
                    'id': f'nonveg_{recipe_id}',
                    'name': recipe_name,
                    'ingredients': [ing.strip() for ing in ingredients.split(',')],
                    'instructions': instructions,
                    'nutrition': {
                        'calories': calories,
                        'protein': protein,
                        'carbs': carbs,
                        'fat': fat,
                        'fiber': fiber
                    },
                    'category': 'non_vegetarian',
                    'tags': ['non_vegetarian'],
                    'cooking_time': 30
                }

                recipes.append(recipe)

        except Exception as e:
            print(f"Error processing CSV row: {e}")
            pass

    def _guess_category(self, dish_name):
        name = dish_name.lower()
        if 'egg' in name or 'omelette' in name or 'breakfast' in name or 'toast' in name:
            return 'breakfast'
        elif 'chicken' in name or 'shrimp' in name or 'tuna' in name:
            return 'lunch'
        else:
            return 'main_course'
    
    def generate_diet_menu(self, user_input):
        """
        Generate a personalized Telugu diet menu based on user input
        """
        try:
            # Parse user input
            preferences = self._parse_user_input(user_input)
            
            # Get available recipes based on diet type
            if preferences['diet_type'] == 'vegetarian':
                all_recipes = self._load_veg_recipes()
            elif preferences['diet_type'] == 'non_vegetarian':
                all_recipes = self._load_non_veg_recipes()
            else:
                # Default to non-vegetarian for backward compatibility
                all_recipes = self._load_non_veg_recipes()

            # Ensure we have recipes loaded
            if not all_recipes:
                return {'error': f'No {preferences["diet_type"]} recipes available'}
            
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
            print(f"Error in generate_diet_menu: {str(e)}")
            return {
                'error': f'ఆహార పట్టిక తయారీ విఫలమైంది: {str(e)}',
                'meal_plan': {},
                'nutrition_summary': {},
                'recommendations': []
            }
    
    def _parse_user_input(self, user_input):
        """Parse user input to extract preferences"""
        preferences = {
            'diet_type': 'non_vegetarian',  # Force non-vegetarian
            'health_goal': 'energy_boost',
            'duration': 7,
            'meals_per_day': 3,
            'calorie_limit': 2000,
            'calorie_target': 2000,  # Add this for compatibility
            'allergies': []
        }
        
        user_input_lower = user_input.lower()
        
        # Extract health goals
        if 'weight_loss' in user_input_lower or 'weight loss' in user_input_lower:
            preferences['health_goal'] = 'weight_loss'
        elif 'weight_gain' in user_input_lower or 'weight gain' in user_input_lower:
            preferences['health_goal'] = 'weight_gain'
        elif 'diabetic' in user_input_lower or 'diabetes' in user_input_lower:
            preferences['health_goal'] = 'diabetic'
        elif 'protein' in user_input_lower:
            preferences['health_goal'] = 'protein_rich'
        
        # Extract meals per day
        if '4 meals' in user_input_lower:
            preferences['meals_per_day'] = 4
        elif '5 meals' in user_input_lower:
            preferences['meals_per_day'] = 5
        
        # Extract calorie limit
        import re
        calorie_match = re.search(r'(\d+)\s*calories?', user_input_lower)
        if calorie_match:
            calorie_value = int(calorie_match.group(1))
            preferences['calorie_limit'] = calorie_value
            preferences['calorie_target'] = calorie_value  # Set both for compatibility
        
        # Extract duration
        if 'week' in user_input_lower:
            preferences['duration'] = 7
        elif 'month' in user_input_lower:
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
                    meal = self._select_meal(recipes, meal_type, selected_recipes_ids)

                    # Try to avoid duplicates within the same day if we have enough recipes
                    if meal and len(recipes) > preferences['meals_per_day']:
                        attempts = 0
                        while meal.get('id') in selected_recipes_ids and attempts < 3:
                            meal = self._select_meal(recipes, meal_type, selected_recipes_ids)
                            attempts += 1

                    meal_plan[day_key]['meals'][meal_type] = meal
                    if meal:
                        selected_recipes_ids.add(meal.get('id'))

            if preferences['meals_per_day'] >= 4:
                snack = self._select_meal(recipes, 'snack', selected_recipes_ids)

                # Try to avoid duplicates if possible
                if snack and len(recipes) > preferences['meals_per_day']:
                    attempts = 0
                    while snack.get('id') in selected_recipes_ids and attempts < 3:
                        snack = self._select_meal(recipes, 'snack', selected_recipes_ids)
                        attempts += 1

                meal_plan[day_key]['meals']['snack'] = snack
                if snack:
                    selected_recipes_ids.add(snack.get('id'))
            
            # Reset random seed after each day
            random.seed()
        
        return meal_plan
    
    
    def _select_meal(self, recipes, meal_type, used_recipes=None):
        """Select a meal from available non-vegetarian recipes with enhanced randomization"""
        if used_recipes is None:
            used_recipes = set()

        # Enhanced randomization with multiple entropy sources
        import time
        import hashlib

        # Create a unique seed based on current time, meal type, and used recipes
        entropy_string = f"{time.time()}_{meal_type}_{len(used_recipes)}_{random.random()}"
        seed_hash = hashlib.md5(entropy_string.encode()).hexdigest()
        seed_value = int(seed_hash[:8], 16) % 100000
        random.seed(seed_value)

        # Enhanced filtering for better variety
        # 1. First try recipes not used in this session
        available_recipes = [r for r in recipes if r['id'] not in used_recipes]

        # 2. If we have enough unused recipes, use them
        if len(available_recipes) >= 3:
            pass  # Use unused recipes
        else:
            # 3. If running low on unused recipes, include all but prefer unused ones
            unused_recipes = [r for r in recipes if r['id'] not in used_recipes]
            used_recipes_list = [r for r in recipes if r['id'] in used_recipes]

            # Shuffle both lists for randomness
            random.shuffle(unused_recipes)
            random.shuffle(used_recipes_list)

            # Combine with unused recipes first
            available_recipes = unused_recipes + used_recipes_list

        if not available_recipes:
            available_recipes = recipes  # Reset if all recipes used

        # Shuffle the available recipes for better variety
        random.shuffle(available_recipes)

        # Select based on meal type preferences
        if meal_type == 'breakfast':
            # Prefer lighter, egg-based dishes for breakfast
            breakfast_preferred = [r for r in available_recipes
                                 if any(word in r['name'].lower()
                                       for word in ['egg', 'omelet', 'boiled'])]
            if breakfast_preferred:
                selected = random.choice(breakfast_preferred)
            else:
                selected = random.choice(available_recipes)

        elif meal_type == 'lunch':
            # Prefer heartier dishes for lunch
            lunch_preferred = [r for r in available_recipes
                              if r['nutrition']['calories'] >= 300]
            if lunch_preferred:
                selected = random.choice(lunch_preferred)
            else:
                selected = random.choice(available_recipes)

        elif meal_type == 'dinner':
            # Prefer moderate calorie dishes for dinner
            dinner_preferred = [r for r in available_recipes
                               if 250 <= r['nutrition']['calories'] <= 400]
            if dinner_preferred:
                selected = random.choice(dinner_preferred)
            else:
                selected = random.choice(available_recipes)

        elif meal_type == 'snack':
            # Prefer lighter dishes for snacks
            snack_preferred = [r for r in available_recipes
                              if r['nutrition']['calories'] < 300]
            if snack_preferred:
                selected = random.choice(snack_preferred)
            else:
                selected = random.choice(available_recipes)

        else:
            selected = random.choice(available_recipes)

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
        
        # Calculate averages per meal and per day
        days_count = len(meal_plan)

        if meal_count > 0:
            avg_per_meal = {}
            avg_per_day = {}

            for key in total_nutrition:
                avg_per_meal[key] = round(total_nutrition[key] / meal_count, 1)
                avg_per_day[key] = round(total_nutrition[key] / days_count, 1) if days_count > 0 else 0

            # Return both formats for compatibility
            return {
                **avg_per_meal,  # For backward compatibility
                'avg_calories_per_day': avg_per_day['calories'],
                'avg_protein_per_day': avg_per_day['protein'],
                'avg_carbs_per_day': avg_per_day['carbs'],
                'avg_fat_per_day': avg_per_day['fat'],
                'avg_fiber_per_day': avg_per_day['fiber'],
                'total_calories': total_nutrition['calories'],
                'total_protein': total_nutrition['protein'],
                'meal_count': meal_count,
                'days_count': days_count
            }

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

    def _create_sample_nonveg_recipes(self):
        """Create sample non-vegetarian recipes as fallback - NO VEGETARIAN RECIPES"""
        return [
            {
                'id': 'nonveg_chicken_curry',
                'name': 'Chicken Curry',
                'ingredients': ['500g chicken', '2 onions', '3 tomatoes', '1 tbsp ginger-garlic paste', 'spices'],
                'nutrition': {'calories': 350, 'protein': 25, 'carbs': 15, 'fat': 20, 'fiber': 3},
                'instructions': 'Cook chicken with spices and vegetables until tender',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 45
            },
            {
                'id': 'nonveg_egg_curry',
                'name': 'Egg Curry',
                'ingredients': ['6 eggs', '2 onions', '2 tomatoes', '1 tbsp oil', 'curry leaves'],
                'nutrition': {'calories': 280, 'protein': 18, 'carbs': 12, 'fat': 18, 'fiber': 2},
                'instructions': 'Boil eggs and cook in spicy gravy',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 30
            },
            {
                'id': 'nonveg_fish_fry',
                'name': 'Fish Fry',
                'ingredients': ['500g fish', '1 tbsp red chili powder', '1 tsp turmeric', 'oil for frying'],
                'nutrition': {'calories': 320, 'protein': 30, 'carbs': 5, 'fat': 18, 'fiber': 1},
                'instructions': 'Marinate fish and deep fry until golden',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 25
            },
            {
                'id': 'nonveg_mutton_biryani',
                'name': 'Mutton Biryani',
                'ingredients': ['500g mutton', '2 cups basmati rice', '1 cup yogurt', 'biryani spices'],
                'nutrition': {'calories': 450, 'protein': 28, 'carbs': 45, 'fat': 22, 'fiber': 2},
                'instructions': 'Layer cooked mutton and rice, cook on dum',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 90
            },
            {
                'id': 'nonveg_egg_omelet',
                'name': 'Masala Omelet',
                'ingredients': ['3 eggs', '1 onion', '2 green chilies', '1 tomato', 'coriander leaves'],
                'nutrition': {'calories': 220, 'protein': 15, 'carbs': 8, 'fat': 14, 'fiber': 2},
                'instructions': 'Beat eggs with vegetables and cook as omelet',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 10
            },
            {
                'id': 'nonveg_chicken_biryani',
                'name': 'Chicken Biryani',
                'ingredients': ['500g chicken', '2 cups basmati rice', '1 cup yogurt', 'biryani spices'],
                'nutrition': {'calories': 420, 'protein': 26, 'carbs': 42, 'fat': 18, 'fiber': 2},
                'instructions': 'Layer cooked chicken and rice, cook on dum',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 75
            },
            {
                'id': 'nonveg_prawn_curry',
                'name': 'Prawn Curry',
                'ingredients': ['500g prawns', '1 coconut', '2 onions', '3 tomatoes', 'curry spices'],
                'nutrition': {'calories': 300, 'protein': 22, 'carbs': 18, 'fat': 16, 'fiber': 3},
                'instructions': 'Cook prawns in coconut curry',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 35
            },
            {
                'id': 'nonveg_chicken_tikka',
                'name': 'Chicken Tikka',
                'ingredients': ['500g chicken', '1 cup yogurt', '1 tbsp garam masala', '1 tbsp ginger-garlic paste'],
                'nutrition': {'calories': 290, 'protein': 35, 'carbs': 8, 'fat': 12, 'fiber': 1},
                'instructions': 'Marinate chicken and grill until cooked',
                'category': 'non_vegetarian',
                'tags': ['non_vegetarian'],
                'cooking_time': 40
            }
        ]
