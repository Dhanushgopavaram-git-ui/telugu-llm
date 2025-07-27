import requests
import json
from config import NUTRITION_API_KEY, NUTRITION_API_URL

class NutritionAPI:
    def __init__(self):
        self.api_key = NUTRITION_API_KEY
        self.api_url = NUTRITION_API_URL
    
    def get_nutrition_data(self, ingredients):
        """
        Get nutrition data for a list of ingredients
        Uses Edamam Nutrition API
        """
        if not self.api_key:
            # Return mock data if no API key is provided
            return self._get_mock_nutrition_data(ingredients)
        
        try:
            # Prepare ingredients for API call
            ingredient_text = " & ".join(ingredients)
            
            params = {
                'app_id': 'your-app-id',  # You'll need to register at Edamam
                'app_key': self.api_key,
                'ingr': ingredient_text
            }
            
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_nutrition_response(data)
            
        except requests.RequestException as e:
            print(f"Error fetching nutrition data: {e}")
            return self._get_mock_nutrition_data(ingredients)
    
    def _parse_nutrition_response(self, data):
        """Parse nutrition API response"""
        try:
            # This is a simplified parser - adjust based on actual API response
            nutrition = {
                'calories': data.get('calories', 0),
                'protein': data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0),
                'carbs': data.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity', 0),
                'fat': data.get('totalNutrients', {}).get('FAT', {}).get('quantity', 0),
                'fiber': data.get('totalNutrients', {}).get('FIBTG', {}).get('quantity', 0),
                'sugar': data.get('totalNutrients', {}).get('SUGAR', {}).get('quantity', 0),
                'sodium': data.get('totalNutrients', {}).get('NA', {}).get('quantity', 0)
            }
            return nutrition
        except Exception as e:
            print(f"Error parsing nutrition data: {e}")
            return self._get_mock_nutrition_data([])
    
    def _get_mock_nutrition_data(self, ingredients):
        """Generate mock nutrition data for testing"""
        # Calculate approximate nutrition based on common ingredients
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        total_sugar = 0
        total_sodium = 0
        
        # Common Telugu ingredients and their approximate nutrition per 100g
        ingredient_nutrition = {
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sugar': 0.1, 'sodium': 1},
            'tamarind': {'calories': 239, 'protein': 2.8, 'carbs': 62.5, 'fat': 0.6, 'fiber': 5.1, 'sugar': 57.4, 'sodium': 28},
            'turmeric': {'calories': 354, 'protein': 8, 'carbs': 65, 'fat': 10, 'fiber': 21, 'sugar': 3.2, 'sodium': 38},
            'chili': {'calories': 40, 'protein': 1.9, 'carbs': 8.8, 'fat': 0.4, 'fiber': 1.5, 'sugar': 5.3, 'sodium': 7},
            'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7, 'sugar': 4.7, 'sodium': 4},
            'oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'fiber': 0, 'sugar': 0, 'sodium': 0},
            'salt': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0, 'sodium': 38758},
            'mustard': {'calories': 508, 'protein': 26, 'carbs': 28, 'fat': 36, 'fiber': 12, 'sugar': 6.8, 'sodium': 5},
            'curry': {'calories': 325, 'protein': 14, 'carbs': 58, 'fat': 14, 'fiber': 33, 'sugar': 2.8, 'sodium': 52},
            'coriander': {'calories': 23, 'protein': 2.1, 'carbs': 3.7, 'fat': 0.5, 'fiber': 2.8, 'sugar': 0.9, 'sodium': 46}
        }
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower()
            for key, nutrition in ingredient_nutrition.items():
                if key in ingredient_lower:
                    # Assume 50g per ingredient for calculation
                    total_calories += nutrition['calories'] * 0.5
                    total_protein += nutrition['protein'] * 0.5
                    total_carbs += nutrition['carbs'] * 0.5
                    total_fat += nutrition['fat'] * 0.5
                    total_fiber += nutrition['fiber'] * 0.5
                    total_sugar += nutrition['sugar'] * 0.5
                    total_sodium += nutrition['sodium'] * 0.5
                    break
        
        # Ensure minimum values
        if total_calories == 0:
            total_calories = 250  # Default calories for a typical dish
        
        return {
            'calories': round(total_calories, 1),
            'protein': round(total_protein, 1),
            'carbs': round(total_carbs, 1),
            'fat': round(total_fat, 1),
            'fiber': round(total_fiber, 1),
            'sugar': round(total_sugar, 1),
            'sodium': round(total_sodium, 1)
        } 