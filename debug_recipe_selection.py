#!/usr/bin/env python3
"""
Debug why certain recipes are not being selected
"""

from diet_generator import TeluguDietGenerator

def debug_meal_selection():
    print("🔍 Debugging Meal Selection Logic...")
    
    generator = TeluguDietGenerator()
    recipes = generator._load_non_veg_recipes()
    
    # Check what recipes are available for each meal type
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    
    for meal_type in meal_types:
        print(f"\n--- {meal_type.upper()} PREFERENCES ---")
        
        if meal_type == 'breakfast':
            # Prefer lighter, egg-based dishes for breakfast
            preferred = [r for r in recipes
                        if any(word in r['name'].lower()
                              for word in ['egg', 'omelet', 'boiled'])]
            print(f"Breakfast preferred recipes: {len(preferred)}")
            for recipe in preferred[:5]:
                print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")
                
        elif meal_type == 'lunch':
            # Prefer heartier dishes for lunch
            preferred = [r for r in recipes
                        if r['nutrition']['calories'] >= 300]
            print(f"Lunch preferred recipes (>=300 cal): {len(preferred)}")
            for recipe in preferred[:5]:
                print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")
                
        elif meal_type == 'dinner':
            # Prefer moderate calorie dishes for dinner
            preferred = [r for r in recipes
                        if 250 <= r['nutrition']['calories'] <= 400]
            print(f"Dinner preferred recipes (250-400 cal): {len(preferred)}")
            for recipe in preferred[:5]:
                print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")
                
        elif meal_type == 'snack':
            # Prefer lighter dishes for snacks
            preferred = [r for r in recipes
                        if r['nutrition']['calories'] < 300]
            print(f"Snack preferred recipes (<300 cal): {len(preferred)}")
            for recipe in preferred[:5]:
                print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")

def check_boiled_egg_recipes():
    print("\n🥚 Analyzing Boiled Egg Avocado Toast Recipes...")
    
    generator = TeluguDietGenerator()
    recipes = generator._load_non_veg_recipes()
    
    boiled_egg_recipes = [r for r in recipes if 'Boiled Egg Avocado Toast' in r['name']]
    
    print(f"Total Boiled Egg Avocado Toast recipes: {len(boiled_egg_recipes)}")
    
    for recipe in boiled_egg_recipes[:5]:
        print(f"\nRecipe: {recipe['name']}")
        print(f"  Calories: {recipe['nutrition']['calories']}")
        print(f"  Contains 'egg': {'egg' in recipe['name'].lower()}")
        print(f"  Contains 'boiled': {'boiled' in recipe['name'].lower()}")
        print(f"  Suitable for breakfast: {any(word in recipe['name'].lower() for word in ['egg', 'omelet', 'boiled'])}")
        print(f"  Suitable for lunch: {recipe['nutrition']['calories'] >= 300}")
        print(f"  Suitable for dinner: {250 <= recipe['nutrition']['calories'] <= 400}")
        print(f"  Suitable for snack: {recipe['nutrition']['calories'] < 300}")

def test_single_meal_selection():
    print("\n🎯 Testing Single Meal Selection...")
    
    generator = TeluguDietGenerator()
    recipes = generator._load_non_veg_recipes()
    
    # Test breakfast selection multiple times
    breakfast_selections = []
    for i in range(20):
        selected = generator._select_meal(recipes, 'breakfast', set())
        if selected:
            breakfast_selections.append(selected['name'])
    
    print(f"Breakfast selections (20 attempts):")
    unique_breakfast = set(breakfast_selections)
    for dish in unique_breakfast:
        count = breakfast_selections.count(dish)
        print(f"  {dish}: {count} times")
    
    # Check if any Boiled Egg recipes were selected
    boiled_egg_selected = [dish for dish in breakfast_selections if 'Boiled Egg' in dish]
    print(f"\nBoiled Egg recipes selected for breakfast: {len(boiled_egg_selected)}")

if __name__ == "__main__":
    debug_meal_selection()
    check_boiled_egg_recipes()
    test_single_meal_selection()
