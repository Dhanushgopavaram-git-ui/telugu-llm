#!/usr/bin/env python3
"""
Test to ensure all 50 recipes can be used in meal plans
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from streamlit_app import CalorieAwareMealPlanner, create_meal_table
from diet_generator import TeluguDietGenerator

def test_comprehensive_recipe_usage():
    print("🧪 Testing Comprehensive Recipe Usage...")
    
    planner = CalorieAwareMealPlanner()
    generator = TeluguDietGenerator()
    
    # Load all recipes
    all_recipes = planner.load_non_veg_recipes()
    print(f"Total recipes available: {len(all_recipes)}")
    
    # Track recipe usage across multiple generations
    used_recipes = set()
    all_selected_recipes = []
    
    # Generate many meal plans to ensure all recipes get a chance
    for i in range(50):  # Generate 50 meal plans
        print(f"Generating meal plan {i+1}/50...", end='\r')
        
        # Use the enhanced meal planner
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=2000,  # Moderate target
            meals_per_day=3,
            days=2  # 2 days per plan
        )
        
        if meal_plan:
            for day_data in meal_plan.values():
                for meal in day_data['meals'].values():
                    if meal:
                        recipe_name = meal['name']
                        used_recipes.add(recipe_name)
                        all_selected_recipes.append(recipe_name)
    
    print(f"\nResults after 50 meal plan generations:")
    print(f"Total meal selections: {len(all_selected_recipes)}")
    print(f"Unique recipes used: {len(used_recipes)}")
    print(f"Recipe utilization: {len(used_recipes)}/50 ({len(used_recipes)/50*100:.1f}%)")
    
    # Check which recipes were never used
    all_recipe_names = {recipe['name'] for recipe in all_recipes}
    unused_recipes = all_recipe_names - used_recipes
    
    print(f"\nUnused recipes: {len(unused_recipes)}")
    if unused_recipes:
        print("Recipes that were never selected:")
        for recipe in sorted(unused_recipes):
            print(f"  - {recipe}")
    else:
        print("🎉 ALL RECIPES WERE USED!")
    
    # Show usage frequency distribution
    recipe_frequency = {}
    for recipe in all_selected_recipes:
        recipe_frequency[recipe] = recipe_frequency.get(recipe, 0) + 1
    
    # Group by dish type
    dish_type_usage = {}
    for recipe_name, count in recipe_frequency.items():
        dish_type = recipe_name.split('#')[0].strip()
        if dish_type not in dish_type_usage:
            dish_type_usage[dish_type] = {'count': 0, 'recipes': 0}
        dish_type_usage[dish_type]['count'] += count
        dish_type_usage[dish_type]['recipes'] += 1
    
    print(f"\nUsage by dish type:")
    for dish_type, stats in dish_type_usage.items():
        avg_usage = stats['count'] / stats['recipes'] if stats['recipes'] > 0 else 0
        print(f"  {dish_type}: {stats['recipes']} recipes used, avg {avg_usage:.1f} times each")

def test_forced_variety():
    print("\n🔄 Testing Forced Variety System...")
    
    planner = CalorieAwareMealPlanner()
    
    # Generate a single large meal plan to test variety within one plan
    meal_plan = planner.generate_varied_meal_plan(
        total_calories=2000,
        meals_per_day=3,
        days=7  # Full week
    )
    
    if meal_plan:
        meal_table = create_meal_table(meal_plan)
        
        total_meals = len(meal_table)
        unique_dishes = meal_table['Dish'].nunique()
        variety_percentage = (unique_dishes / total_meals) * 100
        
        print(f"Single week meal plan:")
        print(f"  Total meals: {total_meals}")
        print(f"  Unique dishes: {unique_dishes}")
        print(f"  Variety: {variety_percentage:.1f}%")
        
        # Check dish type distribution
        dish_types = meal_table['Dish'].apply(lambda x: x.split('#')[0].strip())
        dish_type_counts = dish_types.value_counts()
        
        print(f"\nDish type distribution in one week:")
        for dish_type, count in dish_type_counts.items():
            print(f"  {dish_type}: {count} meals")
        
        # Show the actual meal plan
        print(f"\nSample meals from the week:")
        for _, row in meal_table.head(10).iterrows():
            print(f"  {row['Day']} {row['Meal Type']}: {row['Dish']} ({row['Calories']} cal)")

def test_calorie_distribution_with_all_recipes():
    print("\n⚖️ Testing Calorie Distribution with All Recipe Types...")
    
    generator = TeluguDietGenerator()
    all_recipes = generator._load_non_veg_recipes()
    
    # Group recipes by calorie ranges
    calorie_groups = {
        'low': [r for r in all_recipes if r['nutrition']['calories'] < 200],
        'medium': [r for r in all_recipes if 200 <= r['nutrition']['calories'] < 300],
        'high': [r for r in all_recipes if r['nutrition']['calories'] >= 300]
    }
    
    print(f"Recipe distribution by calories:")
    for group, recipes in calorie_groups.items():
        dish_types = set(r['name'].split('#')[0].strip() for r in recipes)
        print(f"  {group.title()} calorie ({group}): {len(recipes)} recipes, {len(dish_types)} dish types")
        for dish_type in sorted(dish_types):
            count = len([r for r in recipes if r['name'].startswith(dish_type)])
            print(f"    - {dish_type}: {count} variations")

if __name__ == "__main__":
    test_comprehensive_recipe_usage()
    test_forced_variety()
    test_calorie_distribution_with_all_recipes()
