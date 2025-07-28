#!/usr/bin/env python3
"""
Analyze the vegetarian recipes CSV file
"""

import pandas as pd

def analyze_veg_recipes():
    print("📊 Analyzing Vegetarian Recipes CSV...")
    
    try:
        # Read the CSV file
        df = pd.read_csv('veg_diet_recipes.csv', quotechar='"', skipinitialspace=True, encoding='utf-8')
        
        print(f"Total vegetarian recipes: {len(df)}")
        
        # Check for unique dishes
        unique_dishes = df['Dish'].nunique()
        print(f"Unique dish names: {unique_dishes}")
        
        # Show sample dishes
        print(f"\nSample vegetarian dishes:")
        for i, dish in enumerate(df['Dish'].head(10)):
            print(f"  {i+1}. {dish}")
        
        # Analyze calories
        calories = df['Calories'].dropna()
        print(f"\nCalorie analysis:")
        print(f"  Range: {calories.min()} - {calories.max()}")
        print(f"  Average: {calories.mean():.1f}")
        print(f"  Median: {calories.median():.1f}")
        
        # Calorie distribution
        print(f"\nCalorie distribution:")
        print(f"  < 200 cal: {len(calories[calories < 200])} recipes")
        print(f"  200-300 cal: {len(calories[(calories >= 200) & (calories < 300)])} recipes")
        print(f"  300-400 cal: {len(calories[(calories >= 300) & (calories < 400)])} recipes")
        print(f"  400-500 cal: {len(calories[(calories >= 400) & (calories < 500)])} recipes")
        print(f"  > 500 cal: {len(calories[calories >= 500])} recipes")
        
        # Show high calorie recipes
        high_cal = df[df['Calories'] >= 400].sort_values('Calories', ascending=False)
        print(f"\nHigh-calorie vegetarian recipes (>= 400 cal):")
        for _, row in high_cal.head(5).iterrows():
            print(f"  {row['Dish']}: {row['Calories']} cal")
        
        # Check for preparation instructions
        has_prep = df['Preparation'].notna().sum()
        print(f"\nRecipes with preparation instructions: {has_prep}/{len(df)}")
        
        return len(df), calories.min(), calories.max(), calories.mean()
        
    except Exception as e:
        print(f"Error reading vegetarian CSV: {e}")
        return 0, 0, 0, 0

if __name__ == "__main__":
    analyze_veg_recipes()
