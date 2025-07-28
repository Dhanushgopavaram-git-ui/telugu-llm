#!/usr/bin/env python3
"""
Check the variety and distribution of recipes in the CSV file
"""

import pandas as pd
from diet_generator import TeluguDietGenerator

def analyze_recipe_variety():
    print("🔍 Analyzing Recipe Variety in CSV...")
    
    # Load recipes using the diet generator
    generator = TeluguDietGenerator()
    recipes = generator._load_non_veg_recipes()
    
    print(f"Total recipes loaded: {len(recipes)}")
    
    # Check unique dish names
    dish_names = [recipe['name'] for recipe in recipes]
    unique_dishes = set(dish_names)
    
    print(f"Unique dish names: {len(unique_dishes)}")
    
    # Count occurrences of each dish type
    dish_counts = {}
    for dish in dish_names:
        base_name = dish.split('#')[0].strip()  # Remove #number
        dish_counts[base_name] = dish_counts.get(base_name, 0) + 1
    
    print("\nDish type distribution:")
    for dish_type, count in sorted(dish_counts.items()):
        print(f"  {dish_type}: {count} variations")
    
    # Check calorie distribution
    calories = [recipe['nutrition']['calories'] for recipe in recipes]
    print(f"\nCalorie range: {min(calories)} - {max(calories)}")
    
    # Group by calorie ranges
    low_cal = [r for r in recipes if r['nutrition']['calories'] < 200]
    med_cal = [r for r in recipes if 200 <= r['nutrition']['calories'] < 300]
    high_cal = [r for r in recipes if r['nutrition']['calories'] >= 300]
    
    print(f"Low calorie (<200): {len(low_cal)} recipes")
    print(f"Medium calorie (200-299): {len(med_cal)} recipes")
    print(f"High calorie (>=300): {len(high_cal)} recipes")
    
    # Show sample from each category
    print(f"\nSample low calorie recipes:")
    for recipe in low_cal[:3]:
        print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")
    
    print(f"\nSample medium calorie recipes:")
    for recipe in med_cal[:3]:
        print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")
    
    print(f"\nSample high calorie recipes:")
    for recipe in high_cal[:3]:
        print(f"  - {recipe['name']}: {recipe['nutrition']['calories']} cal")

def test_meal_selection_variety():
    print("\n🎲 Testing Meal Selection Variety...")
    
    generator = TeluguDietGenerator()
    
    # Generate multiple meal plans and track which recipes are used
    used_recipes = set()
    all_selected_recipes = []
    
    for i in range(10):  # Generate 10 meal plans
        result = generator.generate_diet_menu("weight_loss non_vegetarian 3 meals 1500 calories")
        
        if 'meal_plan' in result:
            for day_data in result['meal_plan'].values():
                for meal in day_data['meals'].values():
                    if meal:
                        recipe_name = meal['name']
                        used_recipes.add(recipe_name)
                        all_selected_recipes.append(recipe_name)
    
    print(f"Total meal selections made: {len(all_selected_recipes)}")
    print(f"Unique recipes used: {len(used_recipes)}")
    print(f"Recipe utilization: {len(used_recipes)}/50 ({len(used_recipes)/50*100:.1f}%)")
    
    # Count frequency of each recipe
    recipe_frequency = {}
    for recipe in all_selected_recipes:
        recipe_frequency[recipe] = recipe_frequency.get(recipe, 0) + 1
    
    # Show most and least used recipes
    sorted_recipes = sorted(recipe_frequency.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nMost frequently selected recipes:")
    for recipe, count in sorted_recipes[:5]:
        print(f"  {recipe}: {count} times")
    
    print(f"\nLeast frequently selected recipes:")
    for recipe, count in sorted_recipes[-5:]:
        print(f"  {recipe}: {count} times")
    
    # Check which recipes were never used
    all_recipes = generator._load_non_veg_recipes()
    all_recipe_names = {recipe['name'] for recipe in all_recipes}
    unused_recipes = all_recipe_names - used_recipes
    
    print(f"\nUnused recipes ({len(unused_recipes)}):")
    for recipe in sorted(unused_recipes)[:10]:  # Show first 10
        print(f"  - {recipe}")

if __name__ == "__main__":
    analyze_recipe_variety()
    test_meal_selection_variety()
