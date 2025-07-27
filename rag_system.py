import os
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from database import RecipeDatabase

# For vector embeddings
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# For vector similarity search
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

# For LLM integration
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain.llms import OpenAI
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class TeluguDietRAG:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", openai_api_key: Optional[str] = None):
        self.db = RecipeDatabase()
        self.recipes = self.db.get_all_recipes()
        
        # Initialize embedding model if available
        self.embedding_model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer(model_name)
                print(f"Loaded embedding model: {model_name}")
            except Exception as e:
                print(f"Error loading embedding model: {e}")
        else:
            print("SentenceTransformers not available. Install with: pip install sentence-transformers")
        
        # Initialize FAISS index
        self.index = None
        self.recipe_ids = []
        if FAISS_AVAILABLE and self.embedding_model is not None:
            self._build_index()
        elif not FAISS_AVAILABLE:
            print("FAISS not available. Install with: pip install faiss-cpu or faiss-gpu")
        
        # Initialize OpenAI if available
        if OPENAI_AVAILABLE and openai_api_key:
            openai.api_key = openai_api_key
            self.openai_available = True
        else:
            self.openai_available = False
            if not OPENAI_AVAILABLE:
                print("OpenAI not available. Install with: pip install openai")
            elif not openai_api_key:
                print("OpenAI API key not provided. Set it to use LLM features.")
        
        # Initialize LangChain if available
        self.langchain_available = LANGCHAIN_AVAILABLE
        if LANGCHAIN_AVAILABLE and openai_api_key:
            self.llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        elif LANGCHAIN_AVAILABLE:
            print("LangChain available but OpenAI API key not provided.")
        else:
            print("LangChain not available. Install with: pip install langchain")
    
    def _build_index(self):
        """Build FAISS index from recipe data"""
        if not self.recipes:
            print("No recipes available to build index")
            return
        
        # Prepare recipe texts for embedding
        texts = []
        self.recipe_ids = []
        
        for recipe in self.recipes:
            # Create a rich text representation of the recipe
            recipe_text = f"{recipe['name']}. "
            recipe_text += f"Category: {recipe.get('category', '')}. "
            recipe_text += f"Tags: {', '.join(recipe.get('tags', []))}. "
            recipe_text += f"Ingredients: {', '.join(recipe['ingredients'])}. "
            
            texts.append(recipe_text)
            self.recipe_ids.append(recipe['id'])
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity with normalized vectors
        self.index.add(embeddings)
        
        print(f"Built FAISS index with {len(texts)} recipes")
    
    def search_recipes(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for recipes similar to the query"""
        if self.index is None or self.embedding_model is None:
            print("Search index not available")
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search index
        scores, indices = self.index.search(query_embedding, k)
        
        # Get recipes
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.recipe_ids):
                recipe_id = self.recipe_ids[idx]
                recipe = next((r for r in self.recipes if r['id'] == recipe_id), None)
                if recipe:
                    recipe['similarity_score'] = float(scores[0][i])
                    results.append(recipe)
        
        return results
    
    def generate_diet_plan(self, user_input: str, lang: str = 'telugu') -> Dict[str, Any]:
        """Generate a diet plan based on user input using RAG"""
        # Extract dietary preferences from user input
        preferences = self._parse_user_input(user_input)
        
        # Search for relevant recipes
        search_query = f"{preferences['health_goal']} {preferences['diet_type']} recipes"
        relevant_recipes = self.search_recipes(search_query, k=20)
        
        # Filter recipes based on preferences
        filtered_recipes = self._filter_recipes(relevant_recipes, preferences)
        
        # Generate meal plan
        meal_plan = self._create_meal_plan(filtered_recipes, preferences)
        
        # Calculate nutrition summary
        nutrition_summary = self._calculate_nutrition_summary(meal_plan)
        
        # Generate recommendations using LLM if available
        if self.openai_available or self.langchain_available:
            recommendations = self._generate_llm_recommendations(preferences, lang)
        else:
            # Fallback to rule-based recommendations
            recommendations = self._generate_rule_based_recommendations(preferences, lang)
        
        return {
            'meal_plan': meal_plan,
            'nutrition_summary': nutrition_summary,
            'recommendations': recommendations,
            'preferences': preferences
        }
    
    def _parse_user_input(self, user_input: str) -> Dict[str, Any]:
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
        if any(word in user_input.lower() for word in ['non-veg', 'non veg', 'meat', 'chicken', 'మాంసాహారం']):
            preferences['diet_type'] = 'non_vegetarian'
        elif any(word in user_input.lower() for word in ['vegan', 'strict vegetarian']):
            preferences['diet_type'] = 'vegan'
        elif any(word in user_input.lower() for word in ['vegetarian', 'శాకాహారం']):
            preferences['diet_type'] = 'vegetarian'
        
        # Extract health goals
        if any(word in user_input.lower() for word in ['diabetic', 'diabetes', 'sugar', 'మధుమేహం']):
            preferences['health_goal'] = 'diabetic'
        elif any(word in user_input.lower() for word in ['weight loss', 'lose weight', 'slim', 'బరువు తగ్గాలి']):
            preferences['health_goal'] = 'weight_loss'
        elif any(word in user_input.lower() for word in ['weight gain', 'gain weight', 'bulk', 'బరువు పెరగాలి']):
            preferences['health_goal'] = 'weight_gain'
        elif any(word in user_input.lower() for word in ['energy', 'strength', 'శక్తివంతమైన']):
            preferences['health_goal'] = 'energy_boost'
        
        # Extract calorie target
        import re
        calorie_match = re.search(r'(\d+)\s*calorie', user_input.lower())
        if calorie_match:
            preferences['calorie_target'] = int(calorie_match.group(1))
        
        # Extract meals per day
        meals_match = re.search(r'(\d+)\s*meals', user_input.lower())
        if meals_match:
            preferences['meals_per_day'] = int(meals_match.group(1))
        
        # Extract allergies
        if 'allergies' in user_input.lower():
            allergies_match = re.search(r'allergies:?\s*([^\n]+)', user_input.lower())
            if allergies_match:
                allergies_text = allergies_match.group(1).strip()
                preferences['allergies'] = [a.strip() for a in allergies_text.split(',')]
        
        return preferences
    
    def _filter_recipes(self, recipes: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter recipes based on user preferences"""
        filtered = []
        
        for recipe in recipes:
            # Check diet type using tags
            if preferences['diet_type'] == 'vegetarian':
                if 'non_vegetarian' in recipe.get('tags', []):
                    continue
            elif preferences['diet_type'] == 'vegan':
                if any(tag in recipe.get('tags', []) for tag in ['non_vegetarian', 'dairy']):
                    continue
            
            # Check health goals using tags and nutrition
            if preferences['health_goal'] == 'diabetic':
                sugar = recipe['nutrition'].get('sugar') if recipe.get('nutrition') else 0
                if sugar and sugar > 20:  # High sugar content
                    continue
            elif preferences['health_goal'] == 'weight_loss':
                calories = recipe['nutrition'].get('calories') if recipe.get('nutrition') else 0
                if calories and calories > 400:  # High calorie
                    continue
            elif preferences['health_goal'] == 'weight_gain':
                calories = recipe['nutrition'].get('calories') if recipe.get('nutrition') else 0
                if calories and calories < 300:  # Low calorie
                    continue
            elif preferences['health_goal'] == 'energy_boost':
                carbs = recipe['nutrition'].get('carbs') if recipe.get('nutrition') else 0
                protein = recipe['nutrition'].get('protein') if recipe.get('nutrition') else 0
                if (carbs and carbs < 30) or (protein and protein < 10):  # Low energy
                    continue
            
            # Check for allergies
            if preferences['allergies']:
                ingredients_text = ' '.join(recipe.get('ingredients', [])).lower()
                if any(allergy.lower() in ingredients_text for allergy in preferences['allergies']):
                    continue
            
            filtered.append(recipe)
        
        return filtered
    
    def _create_meal_plan(self, recipes: List[Dict[str, Any]], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create a meal plan for the specified duration"""
        import random
        from datetime import datetime, timedelta
        
        meal_plan = {}
        
        for day in range(1, preferences['duration'] + 1):
            date = datetime.now() + timedelta(days=day-1)
            day_key = date.strftime('%Y-%m-%d')
            
            meal_plan[day_key] = {
                'day': day,
                'date': date.strftime('%A, %B %d'),
                'telugu_date': self._get_telugu_date(date),
                'meals': {}
            }
            
            # Generate meals for the day
            if preferences['meals_per_day'] >= 3:
                meal_plan[day_key]['meals']['breakfast'] = self._select_meal(recipes, 'breakfast', preferences)
                meal_plan[day_key]['meals']['lunch'] = self._select_meal(recipes, 'lunch', preferences)
                meal_plan[day_key]['meals']['dinner'] = self._select_meal(recipes, 'dinner', preferences)
            
            if preferences['meals_per_day'] >= 4:
                meal_plan[day_key]['meals']['snack'] = self._select_meal(recipes, 'snack', preferences)
        
        return meal_plan
    
    def _select_meal(self, recipes: List[Dict[str, Any]], meal_type: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate recipe for a meal type"""
        import random
        
        suitable_recipes = []
        
        for recipe in recipes:
            # Use category and tags for better meal selection
            if meal_type == 'breakfast':
                if (recipe.get('category') == 'breakfast' or 
                    'breakfast' in recipe.get('tags', []) or
                    (recipe.get('cooking_time', 0) <= 20)):
                    suitable_recipes.append(recipe)
            
            elif meal_type == 'lunch':
                if (recipe.get('category') == 'main_course' or
                    recipe.get('nutrition', {}).get('calories', 0) >= 300):
                    suitable_recipes.append(recipe)
            
            elif meal_type == 'dinner':
                if (recipe.get('category') == 'main_course' or
                    recipe.get('nutrition', {}).get('calories', 0) <= 400):
                    suitable_recipes.append(recipe)
            
            elif meal_type == 'snack':
                if (recipe.get('category') == 'snack' or
                    'snack' in recipe.get('tags', []) or
                    recipe.get('nutrition', {}).get('calories', 0) <= 200):
                    suitable_recipes.append(recipe)
        
        if suitable_recipes:
            return random.choice(suitable_recipes)
        elif recipes:
            return random.choice(recipes)
        else:
            return None
    
    def _calculate_nutrition_summary(self, meal_plan: Dict[str, Any]) -> Dict[str, float]:
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
    
    def _generate_llm_recommendations(self, preferences: Dict[str, Any], lang: str = 'telugu') -> List[str]:
        """Generate recommendations using LLM"""
        if self.openai_available:
            # Use OpenAI directly
            prompt = self._create_recommendation_prompt(preferences, lang)
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7
                )
                recommendations_text = response.choices[0].text.strip()
                recommendations = [r.strip() for r in recommendations_text.split('\n') if r.strip()]
                return recommendations
            except Exception as e:
                print(f"Error generating recommendations with OpenAI: {e}")
                return self._generate_rule_based_recommendations(preferences, lang)
        
        elif self.langchain_available and hasattr(self, 'llm'):
            # Use LangChain
            prompt_template = self._create_recommendation_prompt(preferences, lang)
            prompt = PromptTemplate(template=prompt_template, input_variables=[])
            chain = LLMChain(llm=self.llm, prompt=prompt)
            try:
                recommendations_text = chain.run({})
                recommendations = [r.strip() for r in recommendations_text.split('\n') if r.strip()]
                return recommendations
            except Exception as e:
                print(f"Error generating recommendations with LangChain: {e}")
                return self._generate_rule_based_recommendations(preferences, lang)
        
        else:
            return self._generate_rule_based_recommendations(preferences, lang)
    
    def _create_recommendation_prompt(self, preferences: Dict[str, Any], lang: str = 'telugu') -> str:
        """Create a prompt for LLM recommendation generation"""
        if lang == 'telugu':
            prompt = f"""తెలుగులో ఆరోగ్య సలహాలు ఇవ్వండి. ఈ క్రింది ఆహార ప్రాధాన్యతలు ఉన్న వ్యక్తికి 5-7 ఆరోగ్య సలహాలు ఇవ్వండి:

ఆహార లక్ష్యం: {preferences['health_goal']}
ఆహార రకం: {preferences['diet_type']}
రోజుకు కేలరీలు: {preferences['calorie_target']}

ప్రతి సలహా ఒక పేరాగ్రాఫ్‌లో ఉండాలి. ప్రతి సలహా ఒక వాక్యంతో ప్రారంభించాలి.
"""
        else:
            prompt = f"""Provide health recommendations in Telugu. Give 5-7 health recommendations for a person with the following dietary preferences:

Dietary Goal: {preferences['health_goal']}
Diet Type: {preferences['diet_type']}
Daily Calories: {preferences['calorie_target']}

Each recommendation should be in a separate paragraph. Each recommendation should start with a sentence.
"""
        
        return prompt
    
    def _generate_rule_based_recommendations(self, preferences: Dict[str, Any], lang: str = 'telugu') -> List[str]:
        """Generate rule-based recommendations based on preferences"""
        recommendations = []
        
        # Diet type recommendations
        if preferences['diet_type'] == 'vegetarian':
            if lang == 'telugu':
                recommendations.append("శాకాహార ఆహారం తీసుకోవడం వల్ల హృదయ ఆరోగ్యం మెరుగవుతుంది")
                recommendations.append("ప్రతి రోజు కూరగాయలు మరియు పండ్లు తీసుకోవాలి")
                recommendations.append("పప్పులు మరియు బీన్స్ తీసుకోవడం వల్ల ప్రోటీన్ లభిస్తుంది")
            else:
                recommendations.append("Vegetarian diet improves heart health")
                recommendations.append("Take vegetables and fruits every day")
                recommendations.append("Lentils and beans provide protein")
        
        elif preferences['diet_type'] == 'vegan':
            if lang == 'telugu':
                recommendations.append("శుద్ధ శాకాహార ఆహారం తీసుకోవడం వల్ల ఆరోగ్యం మెరుగవుతుంది")
                recommendations.append("బాదం పప్పు మరియు సోయా ఉత్పత్తులు తీసుకోవాలి")
            else:
                recommendations.append("Pure vegetarian diet improves health")
                recommendations.append("Take almonds and soy products")
        
        elif preferences['diet_type'] == 'non_vegetarian':
            if lang == 'telugu':
                recommendations.append("మాంసాహారంలో ప్రోటీన్ ఎక్కువగా ఉంటుంది")
                recommendations.append("చేపలు మరియు కోడి మాంసం ఆరోగ్యకరమైన ఎంపికలు")
            else:
                recommendations.append("Non-vegetarian food is high in protein")
                recommendations.append("Fish and chicken are healthy choices")
        
        # Health goal recommendations
        if preferences['health_goal'] == 'diabetic':
            if lang == 'telugu':
                recommendations.append("చక్కెర మరియు కార్బోహైడ్రేట్ తక్కువగా తీసుకోవాలి")
                recommendations.append("ఫైబర్ ఎక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
                recommendations.append("మెత్తని ఆహారం తీసుకోవాలి")
            else:
                recommendations.append("Take less sugar and carbohydrates")
                recommendations.append("Take food high in fiber")
                recommendations.append("Take soft food")
        
        elif preferences['health_goal'] == 'weight_loss':
            if lang == 'telugu':
                recommendations.append("కేలరీలు తక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
                recommendations.append("నీరు ఎక్కువగా తాగాలి")
                recommendations.append("వ్యాయామం చేయడం మర్చిపోవద్దు")
            else:
                recommendations.append("Take food low in calories")
                recommendations.append("Drink more water")
                recommendations.append("Don't forget to exercise")
        
        elif preferences['health_goal'] == 'weight_gain':
            if lang == 'telugu':
                recommendations.append("ప్రోటీన్ మరియు కేలరీలు ఎక్కువగా ఉన్న ఆహారం తీసుకోవాలి")
                recommendations.append("రోజుకు 5-6 సార్లు తినాలి")
                recommendations.append("బలమైన వ్యాయామం చేయాలి")
            else:
                recommendations.append("Take food high in protein and calories")
                recommendations.append("Eat 5-6 times a day")
                recommendations.append("Do strength training")
        
        elif preferences['health_goal'] == 'energy_boost':
            if lang == 'telugu':
                recommendations.append("ఎక్కువ కేలరీలు ఉన్న ఆహారం తీసుకోవాలి")
                recommendations.append("విటమిన్లు మరియు ఖనిజాలు ఎక్కువగా తీసుకోవాలి")
                recommendations.append("పండ్లు మరియు కూరగాయలు తీసుకోవాలి")
            else:
                recommendations.append("Take food high in calories")
                recommendations.append("Take more vitamins and minerals")
                recommendations.append("Take fruits and vegetables")
        
        # General recommendations
        if lang == 'telugu':
            recommendations.append("ప్రతి రోజు 8 గంటల నిద్ర తీసుకోవాలి")
            recommendations.append("ఆహారాన్ని నెమ్మదిగా మరియు బాగా నమలాలి")
            recommendations.append("ప్రతి రోజు 8-10 గ్లాస్ నీరు తాగాలి")
        else:
            recommendations.append("Take 8 hours of sleep every day")
            recommendations.append("Chew food slowly and well")
            recommendations.append("Drink 8-10 glasses of water every day")
        
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
    
    def answer_nutrition_question(self, question: str, lang: str = 'telugu') -> str:
        """Answer nutrition questions using RAG"""
        if not (self.openai_available or self.langchain_available):
            if lang == 'telugu':
                return "క్షమించండి, ప్రశ్నలకు సమాధానం ఇవ్వడానికి LLM అందుబాటులో లేదు."
            else:
                return "Sorry, LLM is not available to answer questions."
        
        # Search for relevant recipes
        relevant_recipes = self.search_recipes(question, k=5)
        
        # Create context from relevant recipes
        context = "\n\n".join([f"Recipe: {r['name']}\nIngredients: {', '.join(r['ingredients'])}\nNutrition: {r['nutrition']}" 
                            for r in relevant_recipes])
        
        # Create prompt
        if lang == 'telugu':
            prompt = f"""తెలుగులో ఆహార మరియు పోషకాహార ప్రశ్నలకు సమాధానం ఇవ్వండి. ఈ క్రింది సమాచారం ఆధారంగా ప్రశ్నకు సమాధానం ఇవ్వండి:

{context}

ప్రశ్న: {question}

సమాధానం:"""
        else:
            prompt = f"""Answer nutrition and diet questions in Telugu. Based on the information below, answer the question:

{context}

Question: {question}

Answer:"""
        
        try:
            if self.openai_available:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].text.strip()
            elif self.langchain_available and hasattr(self, 'llm'):
                prompt_template = PromptTemplate(template=prompt, input_variables=[])
                chain = LLMChain(llm=self.llm, prompt=prompt_template)
                return chain.run({})
        except Exception as e:
            print(f"Error answering question: {e}")
            if lang == 'telugu':
                return "క్షమించండి, ప్రశ్నకు సమాధానం ఇవ్వడంలో లోపం ఉంది."
            else:
                return "Sorry, there was an error answering the question."