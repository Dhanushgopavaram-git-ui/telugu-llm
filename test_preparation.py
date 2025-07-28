#!/usr/bin/env python3
"""
Test script to verify that preparation instructions are being loaded correctly
"""

from diet_generator import TeluguDietGenerator

def test_preparation_loading():
    print("🧪 Testing Preparation Instructions Loading...")
    
    generator = TeluguDietGenerator()
    
    # Load recipes and check first few for preparation instructions
    recipes = generator._load_non_veg_recipes()
    
    print(f"Loaded {len(recipes)} recipes")
    
    # Check first 5 recipes for preparation instructions
    for i, recipe in enumerate(recipes[:5]):
        print(f"\n--- Recipe {i+1}: {recipe['name']} ---")
        print(f"Has 'instructions' field: {'instructions' in recipe}")
        print(f"Has 'preparation' field: {'preparation' in recipe}")
        
        if 'preparation' in recipe:
            prep = recipe['preparation']
            print(f"Preparation length: {len(prep)} characters")
            print(f"Preparation preview: {prep[:100]}...")
            
            if prep == "N/A" or prep == "Cook as directed":
                print("❌ Generic preparation found")
            else:
                print("✅ Detailed preparation found")
        else:
            print("❌ No preparation field found")

def test_meal_generation():
    print("\n🍽️ Testing Meal Generation with Preparation...")
    
    generator = TeluguDietGenerator()
    
    # Generate a simple meal plan
    result = generator.generate_diet_menu("weight_loss non_vegetarian 3 meals 1500 calories")
    
    if 'error' in result:
        print(f"❌ Error generating meal plan: {result['error']}")
        return
    
    # Check first day's meals for preparation instructions
    first_day = list(result['meal_plan'].keys())[0]
    meals = result['meal_plan'][first_day]['meals']
    
    print(f"Checking meals for {first_day}:")
    
    for meal_type, meal in meals.items():
        if meal:
            print(f"\n{meal_type.title()}: {meal['name']}")
            prep = meal.get('preparation', 'N/A')
            print(f"Preparation: {prep[:100]}...")
            
            if prep == "N/A" or prep == "Cook as directed":
                print("❌ Generic preparation")
            else:
                print("✅ Detailed preparation")

if __name__ == "__main__":
    test_preparation_loading()
    test_meal_generation()
