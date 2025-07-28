#!/usr/bin/env python3
"""
Test script to verify that different inputs generate different meal plans
"""

from diet_generator import TeluguDietGenerator

def test_meal_variety():
    print("🧪 Testing Meal Plan Variety...")
    
    generator = TeluguDietGenerator()
    
    # Test the same input multiple times to see if we get variety
    test_input = "weight_loss non_vegetarian 3 meals 1500 calories"
    
    meal_plans = []
    
    for i in range(5):
        print(f"\n--- Generation {i+1} ---")
        result = generator.generate_diet_menu(test_input)
        
        if 'error' not in result:
            # Extract first day's meals
            first_day = list(result['meal_plan'].keys())[0]
            day_meals = result['meal_plan'][first_day]['meals']
            
            meal_names = []
            for meal_type, meal in day_meals.items():
                if meal:
                    meal_names.append(f"{meal_type}: {meal['name']}")
            
            meal_plans.append(meal_names)
            print(f"Meals: {', '.join(meal_names)}")
        else:
            print(f"Error: {result['error']}")
    
    # Check for variety
    print(f"\n📊 Variety Analysis:")
    unique_plans = set(str(plan) for plan in meal_plans)
    print(f"Generated {len(meal_plans)} plans")
    print(f"Unique plans: {len(unique_plans)}")
    
    if len(unique_plans) > 1:
        print("✅ Good variety - different meal plans generated!")
    else:
        print("❌ Poor variety - same meal plan repeated")
    
    # Show all unique plans
    for i, plan in enumerate(unique_plans, 1):
        print(f"\nPlan {i}: {plan}")

def test_different_goals():
    print("\n🎯 Testing Different Health Goals...")
    
    generator = TeluguDietGenerator()
    
    goals = [
        "weight_loss non_vegetarian 3 meals 1500 calories",
        "weight_gain non_vegetarian 4 meals 2500 calories", 
        "diabetic non_vegetarian 3 meals 2000 calories",
        "energy_boost non_vegetarian 3 meals 2200 calories"
    ]
    
    results = {}
    
    for goal in goals:
        result = generator.generate_diet_menu(goal)
        if 'error' not in result:
            # Get nutrition summary
            nutrition = result['nutrition_summary']
            avg_calories = nutrition['avg_calories_per_day']
            avg_protein = nutrition['avg_protein_per_day']
            
            results[goal.split()[0]] = {
                'calories': avg_calories,
                'protein': avg_protein
            }
            
            print(f"{goal.split()[0]}: {avg_calories:.1f} cal, {avg_protein:.1f}g protein")
    
    # Check if different goals produce different nutrition profiles
    calorie_values = [r['calories'] for r in results.values()]
    protein_values = [r['protein'] for r in results.values()]
    
    if len(set(calorie_values)) > 1 or len(set(protein_values)) > 1:
        print("✅ Different goals produce different nutrition profiles!")
    else:
        print("❌ All goals produce same nutrition profiles")

if __name__ == "__main__":
    test_meal_variety()
    test_different_goals()
