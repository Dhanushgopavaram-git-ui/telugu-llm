import json
from diet_generator import TeluguDietGenerator

def test_new_recipes():
    # Initialize the diet generator
    diet_gen = TeluguDietGenerator()
    
    # Test cases with different diet types and health goals
    test_cases = [
        {
            "name": "Vegetarian Weight Loss",
            "input": "I want a vegetarian diet for weight loss for 3 days",
            "expected": {
                "diet_type": "vegetarian",
                "health_goal": "weight_loss"
            }
        },
        {
            "name": "Non-Vegetarian Weight Gain",
            "input": "I need a non-vegetarian diet for weight gain for 5 days",
            "expected": {
                "diet_type": "non_vegetarian",
                "health_goal": "weight_gain"
            }
        },
        {
            "name": "Vegetarian Diabetic",
            "input": "I am diabetic and need a vegetarian diet for 4 days",
            "expected": {
                "diet_type": "vegetarian",
                "health_goal": "diabetic"
            }
        },
        {
            "name": "Non-Vegetarian Energy Boost",
            "input": "I need an energy boost with a non-vegetarian diet for 3 days",
            "expected": {
                "diet_type": "non_vegetarian",
                "health_goal": "energy_boost"
            }
        },
        {
            "name": "Vegan Protein-Rich",
            "input": "I want a vegan protein-rich diet for 7 days",
            "expected": {
                "diet_type": "vegan",
                "health_goal": "protein_rich"
            }
        }
    ]
    
    results = {}
    
    # Run tests and collect results
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input: {test_case['input']}")
        
        # Generate diet menu
        menu = diet_gen.generate_diet_menu(test_case['input'])
        
        # Extract preferences from the result
        preferences = menu.get('preferences', {})
        diet_type = preferences.get('diet_type', '')
        health_goal = preferences.get('health_goal', '')
        
        print(f"Detected Diet Type: {diet_type}, Health Goal: {health_goal}")
        
        # Count meal types and categories
        meal_counts = {}
        recipe_ids = set()
        meal_plan = menu.get('meal_plan', {})
        
        for day, meals in meal_plan.items():
            for meal_type, recipe in meals.items():
                if recipe:
                    # Handle both dictionary and integer recipe representations
                    if isinstance(recipe, dict):
                        recipe_id = recipe.get('id')
                        category = recipe.get('category', '')
                    elif isinstance(recipe, int):
                        recipe_id = recipe
                        # We don't have category information for integer recipe IDs
                        # Let's use a placeholder
                        category = 'unknown'
                    else:
                        # Skip if recipe is neither dict nor int
                        continue
                    
                    if recipe_id:
                        recipe_ids.add(recipe_id)
                    
                    if category not in meal_counts:
                        meal_counts[category] = 0
                    meal_counts[category] += 1
        
        # Store results
        results[test_case['name']] = {
            "diet_type": diet_type,
            "health_goal": health_goal,
            "meal_counts": meal_counts,
            "unique_recipes": len(recipe_ids),
            "total_meals": sum(meal_counts.values()) if meal_counts else 0,
            "nutrition_summary": menu.get('nutrition_summary', {})
        }
        
        # Print summary
        print(f"Meal Type Counts: {meal_counts}")
        print(f"Unique Recipes: {len(recipe_ids)}")
        print(f"Total Meals: {sum(meal_counts.values()) if meal_counts else 0}")
        
        # Print nutrition summary
        nutrition_summary = menu.get('nutrition_summary', {})
        if nutrition_summary:
            print(f"Average Calories: {nutrition_summary.get('calories', 0)}")
            print(f"Average Protein: {nutrition_summary.get('protein', 0)}g")
            print(f"Average Carbs: {nutrition_summary.get('carbs', 0)}g")
            print(f"Average Fat: {nutrition_summary.get('fat', 0)}g")
    
    # Save results to file
    with open('new_recipes_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nTest results saved to new_recipes_test_results.json")

if __name__ == "__main__":
    test_new_recipes()