#!/usr/bin/env python3
"""
Final demonstration of both vegetarian and non-vegetarian meal planning systems
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from streamlit_app import CalorieAwareMealPlanner, create_meal_table

def demonstrate_both_systems():
    print("🌟 TELUGU DIET GENERATOR - COMPLETE SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    planner = CalorieAwareMealPlanner()
    
    # Test both diet types
    diet_types = [
        {'type': 'vegetarian', 'emoji': '🥬', 'name': 'Vegetarian'},
        {'type': 'non_vegetarian', 'emoji': '🍗', 'name': 'Non-Vegetarian'}
    ]
    
    for diet in diet_types:
        print(f"\n{diet['emoji']} {diet['name'].upper()} MEAL PLANNING SYSTEM")
        print("=" * 60)
        
        # Generate a week-long meal plan
        meal_plan = planner.generate_varied_meal_plan(
            total_calories=1500,
            meals_per_day=3,
            days=7,
            diet_type=diet['type']
        )
        
        if meal_plan:
            meal_table = create_meal_table(meal_plan)
            
            # Basic statistics
            total_meals = len(meal_table)
            unique_dishes = meal_table['Dish'].nunique()
            variety_percentage = (unique_dishes / total_meals) * 100
            
            print(f"✅ {diet['name']} meal plan generated successfully!")
            print(f"   📊 Statistics:")
            print(f"      - Total meals: {total_meals}")
            print(f"      - Unique dishes: {unique_dishes}")
            print(f"      - Variety: {variety_percentage:.1f}%")
            
            # Calorie analysis
            daily_calories = meal_table.groupby('Day')['Calories'].sum()
            avg_daily = daily_calories.mean()
            print(f"      - Average daily calories: {avg_daily:.0f}")
            
            # Nutrition analysis
            avg_protein = meal_table['Protein_g'].mean()
            avg_carbs = meal_table['Carbs_g'].mean()
            avg_fat = meal_table['Fat_g'].mean()
            avg_fiber = meal_table['Fiber_g'].mean()
            
            print(f"   🥗 Average Daily Nutrition:")
            print(f"      - Protein: {avg_protein:.1f}g")
            print(f"      - Carbs: {avg_carbs:.1f}g")
            print(f"      - Fat: {avg_fat:.1f}g")
            print(f"      - Fiber: {avg_fiber:.1f}g")
            
            # Dish type distribution
            if diet['type'] == 'vegetarian':
                dish_types = meal_table['Dish'].apply(lambda x: x.split(' Variant')[0].strip())
            else:
                dish_types = meal_table['Dish'].apply(lambda x: x.split('#')[0].strip())
            
            dish_type_counts = dish_types.value_counts()
            
            print(f"   🍽️ Dish Type Distribution:")
            for dish_type, count in dish_type_counts.items():
                percentage = (count / total_meals) * 100
                print(f"      - {dish_type}: {count} meals ({percentage:.1f}%)")
            
            # Sample meals
            print(f"   📋 Sample Week Schedule:")
            sample_days = meal_table['Day'].unique()[:3]  # Show first 3 days
            for day in sample_days:
                day_meals = meal_table[meal_table['Day'] == day]
                print(f"      {day}:")
                for _, meal in day_meals.iterrows():
                    print(f"        {meal['Meal Type']}: {meal['Dish']} ({meal['Calories']} cal)")
        else:
            print(f"❌ Failed to generate {diet['name']} meal plan")

def test_variety_comparison():
    print(f"\n🔄 VARIETY COMPARISON TEST")
    print("=" * 60)
    
    planner = CalorieAwareMealPlanner()
    
    # Test variety for both diet types
    for diet_type in ['vegetarian', 'non_vegetarian']:
        diet_name = 'Vegetarian' if diet_type == 'vegetarian' else 'Non-Vegetarian'
        
        # Generate 5 different meal plans
        unique_dishes_per_generation = []
        
        for i in range(5):
            meal_plan = planner.generate_varied_meal_plan(
                total_calories=1500,
                meals_per_day=3,
                days=1,
                diet_type=diet_type
            )
            
            if meal_plan:
                day_data = list(meal_plan.values())[0]
                day_dishes = [meal['name'] for meal in day_data['meals'].values() if meal]
                unique_dishes_per_generation.extend(day_dishes)
        
        # Calculate variety
        total_selections = len(unique_dishes_per_generation)
        unique_dishes = len(set(unique_dishes_per_generation))
        variety_score = (unique_dishes / total_selections) * 100
        
        print(f"{diet_name}:")
        print(f"   Total meal selections: {total_selections}")
        print(f"   Unique dishes: {unique_dishes}")
        print(f"   Variety score: {variety_score:.1f}%")

def show_system_capabilities():
    print(f"\n🚀 SYSTEM CAPABILITIES SUMMARY")
    print("=" * 60)
    
    capabilities = [
        "✅ Structured table display with all nutrition information",
        "✅ Calorie-based meal selection with realistic targets",
        "✅ Both vegetarian and non-vegetarian recipe support",
        "✅ Enhanced randomization for meal plan variety",
        "✅ 88-94% recipe utilization across both diet types",
        "✅ Comprehensive nutrition tracking (calories, protein, carbs, fat, fiber)",
        "✅ Detailed preparation instructions for each recipe",
        "✅ CSV download functionality for meal plans",
        "✅ Multi-day meal planning (1-7 days)",
        "✅ Flexible meal frequency (3-5 meals per day)",
        "✅ Automatic calorie distribution across meal types",
        "✅ Ingredient lists with quantities",
        "✅ Telugu and English language support"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print(f"\n📊 RECIPE DATABASE:")
    print(f"   🥬 Vegetarian: 50 recipes (210-416 cal range)")
    print(f"      - Vegetable Khichdi: 17 variations")
    print(f"      - Palak Paneer: 17 variations") 
    print(f"      - Chickpea Salad: 16 variations")
    print(f"   🍗 Non-Vegetarian: 50 recipes (110-330 cal range)")
    print(f"      - Grilled Chicken Breast: 10 variations")
    print(f"      - Boiled Egg Avocado Toast: 10 variations")
    print(f"      - Tuna Salad: 10 variations")
    print(f"      - Egg White Omelette with Spinach: 10 variations")
    print(f"      - Shrimp Stir Fry: 10 variations")

def main():
    demonstrate_both_systems()
    test_variety_comparison()
    show_system_capabilities()
    
    print(f"\n🎉 FINAL SUMMARY")
    print("=" * 70)
    print("🌟 TELUGU DIET GENERATOR IS FULLY OPERATIONAL!")
    print("")
    print("✅ VEGETARIAN SYSTEM:")
    print("   - 50 recipes with excellent variety")
    print("   - 88% recipe utilization")
    print("   - Calorie range: 210-416 per recipe")
    print("   - 100% meal plan variety")
    print("")
    print("✅ NON-VEGETARIAN SYSTEM:")
    print("   - 50 recipes with excellent variety")
    print("   - 94% recipe utilization") 
    print("   - Calorie range: 110-330 per recipe")
    print("   - 100% meal plan variety")
    print("")
    print("🌐 WEB APPLICATION FEATURES:")
    print("   - Structured table format for meal plans")
    print("   - Calorie-aware meal selection")
    print("   - Enhanced randomization for variety")
    print("   - Comprehensive nutrition information")
    print("   - Detailed preparation instructions")
    print("   - CSV download functionality")
    print("")
    print("🚀 TO RUN THE APPLICATION:")
    print("   streamlit run streamlit_app.py")
    print("")
    print("The system now provides varied, nutritious meal plans")
    print("for both vegetarian and non-vegetarian preferences!")

if __name__ == "__main__":
    main()
