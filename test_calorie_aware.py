#!/usr/bin/env python3
"""
Test script to verify the new calorie-aware meal planning system
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from streamlit_app import CalorieAwareMealPlanner, create_meal_table
import pandas as pd

def test_calorie_aware_planning():
    print("🧪 Testing Calorie-Aware Meal Planning System...")
    
    planner = CalorieAwareMealPlanner()
    
    # Test different calorie targets
    test_cases = [
        {"calories": 1500, "meals": 3, "description": "Weight Loss (1500 cal, 3 meals)"},
        {"calories": 2000, "meals": 3, "description": "Maintenance (2000 cal, 3 meals)"},
        {"calories": 2500, "meals": 4, "description": "Weight Gain (2500 cal, 4 meals)"},
        {"calories": 3000, "meals": 5, "description": "High Energy (3000 cal, 5 meals)"}
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['description']} ---")
        
        # Generate meal plan
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=test_case['calories'],
            meals_per_day=test_case['meals'],
            days=3  # Test with 3 days for faster execution
        )
        
        if meal_plan:
            # Create table
            meal_table = create_meal_table(meal_plan)
            
            # Calculate actual totals
            daily_calories = meal_table.groupby('Day')['Calories'].sum()
            avg_daily_calories = daily_calories.mean()
            
            print(f"✅ Meal plan generated successfully")
            print(f"   Target daily calories: {test_case['calories']}")
            print(f"   Actual avg daily calories: {avg_daily_calories:.1f}")
            print(f"   Difference: {abs(avg_daily_calories - test_case['calories']):.1f}")
            print(f"   Total recipes in plan: {len(meal_table)}")
            
            # Check variety
            unique_dishes = meal_table['Dish'].nunique()
            total_dishes = len(meal_table)
            variety_percentage = (unique_dishes / total_dishes) * 100
            
            print(f"   Unique dishes: {unique_dishes}/{total_dishes} ({variety_percentage:.1f}% variety)")
            
            # Show sample meals
            print(f"   Sample meals:")
            for _, row in meal_table.head(3).iterrows():
                print(f"     - {row['Meal Type']}: {row['Dish']} ({row['Calories']} cal)")
                
        else:
            print("❌ Failed to generate meal plan")

def test_variety_across_generations():
    print("\n🔄 Testing Variety Across Multiple Generations...")
    
    planner = CalorieAwareMealPlanner()
    
    # Generate 5 different meal plans with same parameters
    meal_plans = []
    target_calories = 2000
    meals_per_day = 3
    
    for i in range(5):
        print(f"Generating plan {i+1}/5...")
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=target_calories,
            meals_per_day=meals_per_day,
            days=2  # 2 days for faster testing
        )
        
        if meal_plan:
            meal_table = create_meal_table(meal_plan)
            # Get first day's meals as signature
            first_day_meals = meal_table[meal_table['Day'] == 'Day 1']['Dish'].tolist()
            meal_plans.append(first_day_meals)
    
    # Check for variety
    unique_plans = set(str(plan) for plan in meal_plans)
    print(f"\n📊 Variety Analysis:")
    print(f"Generated {len(meal_plans)} plans")
    print(f"Unique plans: {len(unique_plans)}")
    
    if len(unique_plans) > 1:
        print("✅ Good variety - different meal plans generated!")
        for i, plan in enumerate(unique_plans, 1):
            print(f"   Plan {i}: {plan}")
    else:
        print("❌ Poor variety - same meal plan repeated")

def test_calorie_distribution():
    print("\n⚖️ Testing Calorie Distribution Logic...")
    
    planner = CalorieAwareMealPlanner()
    
    # Test calorie distribution for 3 meals
    meal_plan = planner.generate_varied_meal_plan(
        total_calories=2100,  # Easy to calculate percentages
        meals_per_day=3,
        days=1
    )
    
    if meal_plan:
        meal_table = create_meal_table(meal_plan)
        
        print("Expected distribution for 3 meals:")
        print("  Breakfast: 25% (525 cal)")
        print("  Lunch: 40% (840 cal)")
        print("  Dinner: 35% (735 cal)")
        
        print("\nActual distribution:")
        for _, row in meal_table.iterrows():
            percentage = (row['Calories'] / 2100) * 100
            print(f"  {row['Meal Type']}: {percentage:.1f}% ({row['Calories']} cal)")

def test_non_veg_only():
    print("\n🥩 Testing Non-Vegetarian Only Restriction...")
    
    planner = CalorieAwareMealPlanner()
    
    # Load recipes and verify all are non-veg
    recipes = planner.load_non_veg_recipes()
    
    print(f"Loaded {len(recipes)} recipes")
    
    # Check if all recipes are non-vegetarian
    non_veg_count = 0
    sample_dishes = []
    
    for recipe in recipes[:10]:  # Check first 10
        if 'category' in recipe and recipe['category'] == 'non_vegetarian':
            non_veg_count += 1
        sample_dishes.append(recipe['name'])
    
    print(f"Non-vegetarian recipes in sample: {non_veg_count}/10")
    print("Sample dishes:")
    for dish in sample_dishes[:5]:
        print(f"  - {dish}")
    
    if non_veg_count == 10:
        print("✅ All recipes are non-vegetarian")
    else:
        print("❌ Some recipes may not be properly categorized")

if __name__ == "__main__":
    test_calorie_aware_planning()
    test_variety_across_generations()
    test_calorie_distribution()
    test_non_veg_only()
