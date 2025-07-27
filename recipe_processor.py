import re
from database import RecipeDatabase
from nutrition_api import NutritionAPI

class RecipeProcessor:
    def __init__(self):
        self.db = RecipeDatabase()
        self.nutrition_api = NutritionAPI()
    
    def process_all_telugu_recipes(self):
        """Process and add comprehensive Telugu recipes to the database"""
        recipes = [
            # Breakfast Recipes
            {
                'name': 'Idli Sambar',
                'ingredients': [
                    '2 cups idli batter',
                    '1 cup toor dal',
                    '1 onion, chopped',
                    '1 tomato, chopped',
                    '2-3 green chilies',
                    '1/4 tsp turmeric powder',
                    '1/2 tsp mustard seeds',
                    '1/2 tsp cumin seeds',
                    'Curry leaves',
                    'Salt to taste',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Steam idlis in idli maker for 10-12 minutes
                2. For sambar, pressure cook toor dal with turmeric
                3. Heat oil and add mustard seeds, cumin seeds
                4. Add onions, tomatoes, green chilies
                5. Add cooked dal and simmer for 5 minutes
                6. Garnish with coriander leaves
                7. Serve hot idlis with sambar
                ''',
                'cooking_time': 25,
                'difficulty': 'Easy',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'protein', 'breakfast', 'healthy']
            },
            {
                'name': 'Dosa Chutney',
                'ingredients': [
                    '1 cup dosa batter',
                    '1/2 cup coconut',
                    '2-3 green chilies',
                    '1 inch ginger',
                    '1/2 cup coriander leaves',
                    '1/4 cup roasted chana dal',
                    'Salt to taste',
                    'Oil for cooking'
                ],
                'instructions': '''
                1. Spread dosa batter on hot tawa
                2. Cook until golden brown and crispy
                3. For chutney, grind coconut, chilies, ginger
                4. Add coriander leaves and chana dal
                5. Grind to smooth paste with water
                6. Serve hot dosa with chutney
                ''',
                'cooking_time': 15,
                'difficulty': 'Easy',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'breakfast', 'quick']
            },
            {
                'name': 'Pongal',
                'ingredients': [
                    '1 cup rice',
                    '1/2 cup moong dal',
                    '1/4 cup ghee',
                    '1 tsp black pepper',
                    '1 tsp cumin seeds',
                    '1/4 tsp asafoetida',
                    'Curry leaves',
                    'Salt to taste',
                    'Cashews for garnish'
                ],
                'instructions': '''
                1. Wash rice and moong dal together
                2. Pressure cook with 3 cups water for 3 whistles
                3. Heat ghee and add black pepper, cumin seeds
                4. Add asafoetida and curry leaves
                5. Add cooked rice-dal mixture
                6. Mix well and cook for 2-3 minutes
                7. Garnish with cashews
                ''',
                'cooking_time': 30,
                'difficulty': 'Easy',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'protein', 'breakfast', 'traditional']
            },
            {
                'name': 'Upma',
                'ingredients': [
                    '1 cup semolina (rava)',
                    '1 onion, chopped',
                    '2-3 green chilies',
                    '1 inch ginger, chopped',
                    '1/4 cup vegetables',
                    '1 tbsp oil',
                    '1/2 tsp mustard seeds',
                    '1/2 tsp urad dal',
                    'Curry leaves',
                    'Salt to taste',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Dry roast semolina until golden brown
                2. Heat oil and add mustard seeds, urad dal
                3. Add onions, green chilies, ginger
                4. Add vegetables and sauté for 2 minutes
                5. Add 2 cups water and bring to boil
                6. Add roasted semolina and mix well
                7. Cook covered for 5 minutes
                8. Garnish with coriander leaves
                ''',
                'cooking_time': 20,
                'difficulty': 'Easy',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'breakfast', 'quick', 'healthy']
            },
            {
                'name': 'Puri Aloo Curry',
                'ingredients': [
                    '2 cups wheat flour',
                    '1/2 cup water',
                    'Oil for deep frying',
                    '4 potatoes, boiled and mashed',
                    '1 onion, chopped',
                    '2 tomatoes, chopped',
                    '1 tsp ginger-garlic paste',
                    '1/2 tsp turmeric powder',
                    '1 tsp red chili powder',
                    '1 tsp garam masala',
                    'Salt to taste',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Mix flour with water to make soft dough
                2. Rest for 30 minutes
                3. Roll into small circles and deep fry
                4. For curry, heat oil and add onions
                5. Add ginger-garlic paste and tomatoes
                6. Add spices and mashed potatoes
                7. Cook for 5 minutes
                8. Serve hot puris with curry
                ''',
                'cooking_time': 35,
                'difficulty': 'Medium',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'breakfast', 'traditional']
            },
            
            # Main Course - Rice Dishes
            {
                'name': 'Classic Tamarind Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add cooked rice and salt
                6. Mix well and cook for 2-3 minutes
                7. Garnish with coriander leaves
                ''',
                'cooking_time': 15,
                'difficulty': 'Easy',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'rice', 'traditional', 'sour']
            },
            {
                'name': 'Lemon Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '2 tbsp lemon juice',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 green chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal
                2. Add green chilies, curry leaves, and asafoetida
                3. Add turmeric powder and lemon juice
                4. Cook for 1-2 minutes
                5. Add cooked rice and salt
                6. Mix well and cook for 2-3 minutes
                7. Garnish with coriander leaves
                ''',
                'cooking_time': 12,
                'difficulty': 'Easy',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'rice', 'tangy', 'quick']
            },
            {
                'name': 'Coconut Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '1/2 cup grated coconut',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add grated coconut and cook for 1 minute
                6. Add cooked rice and salt
                7. Mix well and cook for 2-3 minutes
                8. Garnish with coriander leaves
                ''',
                'cooking_time': 18,
                'difficulty': 'Medium',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'rice', 'coconut', 'traditional']
            },
            {
                'name': 'Peanut Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '1/4 cup roasted peanuts',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add roasted peanuts and cook for 1 minute
                6. Add cooked rice and salt
                7. Mix well and cook for 2-3 minutes
                8. Garnish with coriander leaves
                ''',
                'cooking_time': 20,
                'difficulty': 'Medium',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'rice', 'protein', 'nutty']
            },
            {
                'name': 'Biryani',
                'ingredients': [
                    '2 cups basmati rice',
                    '1/2 kg chicken/mutton',
                    '2 onions, sliced',
                    '2 tomatoes, chopped',
                    '1 cup yogurt',
                    '2 tbsp ginger-garlic paste',
                    '1 tsp red chili powder',
                    '1 tsp garam masala',
                    '1/2 tsp turmeric powder',
                    'Whole spices (cardamom, cinnamon, cloves)',
                    'Saffron soaked in milk',
                    'Mint and coriander leaves',
                    'Oil and ghee',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Marinate meat with yogurt and spices for 2 hours
                2. Cook rice until 70% done
                3. Heat oil and add whole spices
                4. Add onions and cook until golden
                5. Add marinated meat and cook
                6. Layer rice and meat in a pot
                7. Add saffron milk and herbs
                8. Dum cook for 30 minutes
                ''',
                'cooking_time': 90,
                'difficulty': 'Hard',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['non_vegetarian', 'rice', 'festive', 'rich']
            },
            
            # Curry Dishes
            {
                'name': 'Gongura Pachadi',
                'ingredients': [
                    '2 cups gongura leaves',
                    '1/2 cup tamarind paste',
                    '2-3 green chilies',
                    '1 inch ginger',
                    '1/2 cup roasted chana dal',
                    '1/2 cup roasted sesame seeds',
                    '1 tsp mustard seeds',
                    '1 tsp cumin seeds',
                    'Oil',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Clean and wash gongura leaves
                2. Cook leaves until soft
                3. Grind with tamarind, chilies, ginger
                4. Add roasted dal and sesame seeds
                5. Temper with mustard and cumin seeds
                6. Mix well and serve
                ''',
                'cooking_time': 25,
                'difficulty': 'Easy',
                'category': 'side_dish',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'sour', 'traditional', 'healthy']
            },
            {
                'name': 'Gutti Vankaya',
                'ingredients': [
                    '8 small brinjals',
                    '1 cup roasted peanuts',
                    '1/2 cup sesame seeds',
                    '2-3 green chilies',
                    '1 inch ginger',
                    '1 tsp red chili powder',
                    '1/2 tsp turmeric powder',
                    '1 tsp coriander powder',
                    'Oil for cooking',
                    'Salt to taste',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Make stuffing with ground peanuts, sesame, spices
                2. Slit brinjals and stuff the mixture
                3. Heat oil and add stuffed brinjals
                4. Cook covered for 15-20 minutes
                5. Turn occasionally until tender
                6. Garnish with coriander leaves
                ''',
                'cooking_time': 30,
                'difficulty': 'Medium',
                'category': 'side_dish',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'protein', 'traditional', 'spicy']
            },
            {
                'name': 'Pesarattu',
                'ingredients': [
                    '1 cup green moong dal',
                    '1/4 cup rice',
                    '2-3 green chilies',
                    '1 inch ginger',
                    '1/2 cup onions, chopped',
                    'Oil for cooking',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Soak moong dal and rice for 4 hours
                2. Grind to smooth batter with chilies and ginger
                3. Add salt and mix well
                4. Heat tawa and pour batter
                5. Spread in circular motion
                6. Add chopped onions on top
                7. Cook until golden brown
                8. Serve hot with chutney
                ''',
                'cooking_time': 20,
                'difficulty': 'Easy',
                'category': 'breakfast',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'protein', 'breakfast', 'healthy']
            },
            {
                'name': 'Ragi Mudde',
                'ingredients': [
                    '1 cup ragi flour',
                    '2 cups water',
                    '1/2 cup rice',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Cook rice until soft
                2. Boil water in a pan
                3. Add ragi flour slowly while stirring
                4. Cook until thick consistency
                5. Add cooked rice and mix well
                6. Shape into balls
                7. Serve hot with curry
                ''',
                'cooking_time': 25,
                'difficulty': 'Medium',
                'category': 'main_course',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'healthy', 'traditional', 'nutritious']
            },
            
            # Snacks and Appetizers
            {
                'name': 'Mirchi Bajji',
                'ingredients': [
                    '8-10 green chilies',
                    '1 cup besan (gram flour)',
                    '1/4 cup rice flour',
                    '1/2 tsp red chili powder',
                    '1/2 tsp turmeric powder',
                    '1/2 tsp ajwain',
                    'Oil for deep frying',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Slit chilies and remove seeds
                2. Mix besan, rice flour, and spices
                3. Add water to make thick batter
                4. Stuff chilies with mixture
                5. Dip in batter and deep fry
                6. Fry until golden brown
                7. Serve hot with chutney
                ''',
                'cooking_time': 20,
                'difficulty': 'Easy',
                'category': 'snack',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'spicy', 'snack', 'street_food']
            },
            {
                'name': 'Bonda',
                'ingredients': [
                    '1 cup urad dal',
                    '1/4 cup rice',
                    '2-3 green chilies',
                    '1 inch ginger',
                    '1/2 cup onions, chopped',
                    '1/2 cup coconut, grated',
                    'Oil for deep frying',
                    'Salt to taste'
                ],
                'instructions': '''
                1. Soak urad dal and rice for 4 hours
                2. Grind to smooth batter
                3. Add chopped vegetables and coconut
                4. Mix well and add salt
                5. Heat oil and drop small portions
                6. Fry until golden brown
                7. Serve hot with chutney
                ''',
                'cooking_time': 25,
                'difficulty': 'Easy',
                'category': 'snack',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'protein', 'snack', 'traditional']
            },
            
            # Desserts
            {
                'name': 'Pootharekulu',
                'ingredients': [
                    '1 cup rice flour',
                    '1/2 cup jaggery',
                    '1/4 cup ghee',
                    '1/4 cup coconut, grated',
                    '1/4 cup dry fruits',
                    'Cardamom powder',
                    'Water for batter'
                ],
                'instructions': '''
                1. Make thin rice flour batter
                2. Spread on hot tawa like dosa
                3. Cook until crisp
                4. Spread ghee and jaggery mixture
                5. Add coconut and dry fruits
                6. Roll tightly
                7. Cut into pieces and serve
                ''',
                'cooking_time': 30,
                'difficulty': 'Hard',
                'category': 'dessert',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'sweet', 'traditional', 'festive']
            },
            {
                'name': 'Gavvalu',
                'ingredients': [
                    '1 cup maida (all-purpose flour)',
                    '1/4 cup rice flour',
                    '1/4 cup jaggery',
                    '1/4 cup ghee',
                    '1/2 tsp cardamom powder',
                    'Oil for deep frying',
                    'Water for dough'
                ],
                'instructions': '''
                1. Mix flours and make soft dough
                2. Roll into thin sheets
                3. Cut into small squares
                4. Make shell shapes
                5. Deep fry until golden
                6. Make jaggery syrup
                7. Coat fried pieces
                8. Serve when cooled
                ''',
                'cooking_time': 40,
                'difficulty': 'Medium',
                'category': 'dessert',
                'cuisine_type': 'Telugu',
                'tags': ['vegetarian', 'sweet', 'traditional', 'festive']
            }
        ]
        
        for recipe in recipes:
            # Add recipe to database
            recipe_id = self.db.add_recipe(
                name=recipe['name'],
                ingredients=recipe['ingredients'],
                instructions=recipe['instructions'],
                cooking_time=recipe['cooking_time'],
                difficulty=recipe['difficulty'],
                category=recipe.get('category', 'main_course'),
                cuisine_type=recipe.get('cuisine_type', 'Telugu'),
                tags=recipe.get('tags', [])
            )
            
            # Get nutrition data
            nutrition_data = self.nutrition_api.get_nutrition_data(recipe['ingredients'])
            
            # Add nutrition data to database
            self.db.add_nutrition(recipe_id, nutrition_data)
            
            print(f"Added recipe: {recipe['name']}")
    
    def process_pulihora_recipes(self):
        """Process and add sample Pulihora recipes to the database"""
        # Keep the original pulihora recipes for backward compatibility
        recipes = [
            {
                'name': 'Classic Tamarind Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add cooked rice and salt
                6. Mix well and cook for 2-3 minutes
                7. Garnish with coriander leaves
                ''',
                'cooking_time': 15,
                'difficulty': 'Easy'
            },
            {
                'name': 'Lemon Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '2 tbsp lemon juice',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 green chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal
                2. Add green chilies, curry leaves, and asafoetida
                3. Add turmeric powder and lemon juice
                4. Cook for 1-2 minutes
                5. Add cooked rice and salt
                6. Mix well and cook for 2-3 minutes
                7. Garnish with coriander leaves
                ''',
                'cooking_time': 12,
                'difficulty': 'Easy'
            },
            {
                'name': 'Coconut Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '1/2 cup grated coconut',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add grated coconut and cook for 1 minute
                6. Add cooked rice and salt
                7. Mix well and cook for 2-3 minutes
                8. Garnish with coriander leaves
                ''',
                'cooking_time': 18,
                'difficulty': 'Medium'
            },
            {
                'name': 'Peanut Pulihora',
                'ingredients': [
                    '2 cups cooked rice',
                    '1/4 cup roasted peanuts',
                    '2 tbsp tamarind paste',
                    '1 tbsp oil',
                    '1 tsp mustard seeds',
                    '1 tsp urad dal',
                    '1 tsp chana dal',
                    '2-3 dry red chilies',
                    '1/4 tsp turmeric powder',
                    '1/4 tsp asafoetida',
                    'Salt to taste',
                    'Curry leaves',
                    'Coriander leaves for garnish'
                ],
                'instructions': '''
                1. Heat oil in a pan and add mustard seeds, urad dal, chana dal, and dry red chilies
                2. Add curry leaves and asafoetida
                3. Add tamarind paste and turmeric powder
                4. Cook for 2-3 minutes until oil separates
                5. Add roasted peanuts and cook for 1 minute
                6. Add cooked rice and salt
                7. Mix well and cook for 2-3 minutes
                8. Garnish with coriander leaves
                ''',
                'cooking_time': 20,
                'difficulty': 'Medium'
            }
        ]
        
        for recipe in recipes:
            # Add recipe to database
            recipe_id = self.db.add_recipe(
                name=recipe['name'],
                ingredients=recipe['ingredients'],
                instructions=recipe['instructions'],
                cooking_time=recipe['cooking_time'],
                difficulty=recipe['difficulty']
            )
            
            # Get nutrition data
            nutrition_data = self.nutrition_api.get_nutrition_data(recipe['ingredients'])
            
            # Add nutrition data to database
            self.db.add_nutrition(recipe_id, nutrition_data)
            
            print(f"Added recipe: {recipe['name']}")
    
    def extract_ingredients_from_text(self, text):
        """Extract ingredients from text using regex patterns"""
        # Common patterns for ingredients
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(cup|tbsp|tsp|gram|g|kg|ml|l|oz|pound|lb)s?\s+([a-zA-Z\s]+)',
            r'([a-zA-Z\s]+)\s+(\d+(?:\.\d+)?)\s*(cup|tbsp|tsp|gram|g|kg|ml|l|oz|pound|lb)s?',
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(cup|tbsp|tsp|gram|g|kg|ml|l|oz|pound|lb)s?\s+([a-zA-Z\s]+)'
        ]
        
        ingredients = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    ingredient = ' '.join(match).strip()
                    ingredients.append(ingredient)
        
        return ingredients
    
    def parse_recipe_text(self, text):
        """Parse recipe text and extract structured data"""
        # This is a simplified parser - you can enhance it based on your document structure
        lines = text.split('\n')
        
        recipe_data = {
            'name': '',
            'ingredients': [],
            'instructions': '',
            'cooking_time': None,
            'difficulty': 'Medium',
            'category': 'main_course',
            'tags': []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if 'ingredients' in line.lower():
                current_section = 'ingredients'
                continue
            elif 'instructions' in line.lower() or 'method' in line.lower():
                current_section = 'instructions'
                continue
            elif 'time' in line.lower():
                # Extract cooking time
                time_match = re.search(r'(\d+)\s*(min|hour|hr)', line, re.IGNORECASE)
                if time_match:
                    recipe_data['cooking_time'] = int(time_match.group(1))
                continue
            
            # Process content based on section
            if current_section == 'ingredients':
                if line and not line.startswith('Ingredients'):
                    recipe_data['ingredients'].append(line)
            elif current_section == 'instructions':
                if line and not line.startswith('Instructions'):
                    recipe_data['instructions'] += line + '\n'
            else:
                # Assume it's the recipe name if no section is detected
                if not recipe_data['name']:
                    recipe_data['name'] = line
        
        return recipe_data 