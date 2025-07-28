#!/usr/bin/env python3
"""
Test the enhanced vegetarian meal planning system
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from streamlit_app import CalorieAwareMealPlanner, create_meal_table
from diet_generator import TeluguDietGenerator

def test_vegetarian_recipe_loading():
    print("🥬 Testing Vegetarian Recipe Loading...")
    print("=" * 50)
    
    generator = TeluguDietGenerator()
    
    # Test vegetarian recipe loading
    veg_recipes = generator._load_veg_recipes()
    
    print(f"✅ Loaded {len(veg_recipes)} vegetarian recipes")
    
    if veg_recipes:
        # Show sample recipes
        print(f"\nSample vegetarian recipes:")
        for i, recipe in enumerate(veg_recipes[:5]):
            print(f"  {i+1}. {recipe['name']}: {recipe['nutrition']['calories']} cal")
        
        # Check calorie distribution
        calories = [r['nutrition']['calories'] for r in veg_recipes]
        print(f"\nCalorie analysis:")
        print(f"  Range: {min(calories)} - {max(calories)}")
        print(f"  Average: {sum(calories)/len(calories):.1f}")
        
        # Check dish variety
        dish_types = set()
        for recipe in veg_recipes:
            base_name = recipe['name'].split(' Variant')[0].strip()
            dish_types.add(base_name)
        
        print(f"  Unique dish types: {len(dish_types)}")
        for dish_type in sorted(dish_types):
            count = len([r for r in veg_recipes if r['name'].startswith(dish_type)])
            print(f"    - {dish_type}: {count} variations")
    
    return len(veg_recipes)

def test_vegetarian_meal_planning():
    print(f"\n🍽️ Testing Vegetarian Meal Planning...")
    print("=" * 50)
    
    planner = CalorieAwareMealPlanner()
    
    # Test vegetarian meal plan generation
    meal_plan = planner.generate_varied_meal_plan(
        total_calories=1500,
        meals_per_day=3,
        days=7,
        diet_type='vegetarian'
    )
    
    if meal_plan:
        meal_table = create_meal_table(meal_plan)
        
        print(f"✅ Generated vegetarian meal plan successfully!")
        print(f"   Total meals: {len(meal_table)}")
        print(f"   Unique dishes: {meal_table['Dish'].nunique()}")
        print(f"   Variety: {meal_table['Dish'].nunique()/len(meal_table)*100:.1f}%")
        
        # Check calorie distribution
        daily_calories = meal_table.groupby('Day')['Calories'].sum()
        avg_daily = daily_calories.mean()
        
        print(f"   Average daily calories: {avg_daily:.0f}")
        print(f"   Target: 1500 (difference: {abs(avg_daily - 1500):.0f})")
        
        # Show dish type distribution
        dish_types = meal_table['Dish'].apply(lambda x: x.split(' Variant')[0].strip())
        dish_type_counts = dish_types.value_counts()
        
        print(f"\n   Dish type distribution:")
        for dish_type, count in dish_type_counts.items():
            print(f"     - {dish_type}: {count} meals")
        
        # Show sample meals
        print(f"\n   Sample vegetarian meals:")
        for _, row in meal_table.head(7).iterrows():
            print(f"     {row['Day']} {row['Meal Type']}: {row['Dish']} ({row['Calories']} cal)")
        
        return True
    else:
        print("❌ Failed to generate vegetarian meal plan")
        return False

def test_variety_across_generations():
    print(f"\n🔄 Testing Vegetarian Meal Plan Variety...")
    print("=" * 50)
    
    planner = CalorieAwareMealPlanner()
    
    # Generate multiple meal plans to test variety
    first_day_meals = []
    for i in range(5):
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=1500,
            meals_per_day=3,
            days=1,
            diet_type='vegetarian'
        )
        
        if meal_plan:
            day_data = list(meal_plan.values())[0]
            day_meals = [meal['name'] for meal in day_data['meals'].values() if meal]
            first_day_meals.append(day_meals)
            print(f"   Generation {i+1}: {', '.join(day_meals)}")
    
    # Check variety across generations
    all_dishes = set()
    for meals in first_day_meals:
        all_dishes.update(meals)
    
    print(f"\n   Unique dishes across 5 generations: {len(all_dishes)}")
    print(f"   Variety score: {len(all_dishes)/(len(first_day_meals)*3)*100:.1f}%")
    
    return len(all_dishes) > 10  # Good variety if more than 10 unique dishes

def test_comprehensive_recipe_usage():
    print(f"\n📊 Testing Comprehensive Vegetarian Recipe Usage...")
    print("=" * 50)
    
    planner = CalorieAwareMealPlanner()
    
    # Track recipe usage across multiple generations
    used_recipes = set()
    all_selected_recipes = []
    
    # Generate many meal plans to ensure all recipes get a chance
    for i in range(25):  # Generate 25 meal plans
        print(f"Generating meal plan {i+1}/25...", end='\r')
        
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=1500,
            meals_per_day=3,
            days=2,
            diet_type='vegetarian'
        )
        
        if meal_plan:
            for day_data in meal_plan.values():
                for meal in day_data['meals'].values():
                    if meal:
                        recipe_name = meal['name']
                        used_recipes.add(recipe_name)
                        all_selected_recipes.append(recipe_name)
    
    print(f"\nResults after 25 vegetarian meal plan generations:")
    print(f"Total meal selections: {len(all_selected_recipes)}")
    print(f"Unique recipes used: {len(used_recipes)}")
    print(f"Recipe utilization: {len(used_recipes)}/50 ({len(used_recipes)/50*100:.1f}%)")
    
    # Check which recipes were never used
    all_recipes = planner.load_veg_recipes()
    all_recipe_names = {recipe['name'] for recipe in all_recipes}
    unused_recipes = all_recipe_names - used_recipes
    
    print(f"\nUnused vegetarian recipes: {len(unused_recipes)}")
    if unused_recipes:
        print("Recipes that were never selected:")
        for recipe in sorted(list(unused_recipes)[:10]):  # Show first 10
            print(f"  - {recipe}")
    else:
        print("🎉 ALL VEGETARIAN RECIPES WERE USED!")
    
    return len(used_recipes) / 50  # Return utilization percentage

def main():
    print("🧪 COMPREHENSIVE VEGETARIAN MEAL PLANNING TEST")
    print("=" * 60)
    
    # Test 1: Recipe Loading
    recipe_count = test_vegetarian_recipe_loading()
    
    # Test 2: Meal Planning
    meal_planning_success = test_vegetarian_meal_planning()
    
    # Test 3: Variety Testing
    variety_success = test_variety_across_generations()
    
    # Test 4: Recipe Usage
    utilization = test_comprehensive_recipe_usage()
    
    # Summary
    print(f"\n🎉 VEGETARIAN SYSTEM TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Recipe Loading: {recipe_count} vegetarian recipes loaded")
    print(f"✅ Meal Planning: {'Success' if meal_planning_success else 'Failed'}")
    print(f"✅ Variety: {'Good' if variety_success else 'Needs Improvement'}")
    print(f"✅ Recipe Utilization: {utilization*100:.1f}%")
    
    if recipe_count >= 40 and meal_planning_success and variety_success and utilization >= 0.8:
        print(f"\n🌟 VEGETARIAN MEAL PLANNING SYSTEM IS READY!")
        print(f"   - Excellent recipe variety and utilization")
        print(f"   - Calorie-aware meal selection working")
        print(f"   - Enhanced randomization providing variety")
    else:
        print(f"\n⚠️ System needs improvements:")
        if recipe_count < 40:
            print(f"   - Low recipe count: {recipe_count}")
        if not meal_planning_success:
            print(f"   - Meal planning failed")
        if not variety_success:
            print(f"   - Poor variety across generations")
        if utilization < 0.8:
            print(f"   - Low recipe utilization: {utilization*100:.1f}%")

if __name__ == "__main__":
    main()
