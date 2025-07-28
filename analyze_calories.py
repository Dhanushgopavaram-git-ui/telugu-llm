#!/usr/bin/env python3
"""
Analyze the calorie distribution in the CSV file
"""

import pandas as pd
import matplotlib.pyplot as plt

def analyze_calorie_distribution():
    print("📊 Analyzing Calorie Distribution in CSV...")
    
    # Read the CSV file
    df = pd.read_csv('non_veg_diet_recipes.csv', quotechar='"', skipinitialspace=True, encoding='utf-8')
    
    # Clean and analyze calories
    calories = df['Calories'].dropna()
    
    print(f"Total recipes: {len(df)}")
    print(f"Recipes with calorie data: {len(calories)}")
    print(f"Calorie range: {calories.min()} - {calories.max()}")
    print(f"Average calories: {calories.mean():.1f}")
    print(f"Median calories: {calories.median():.1f}")
    
    # Show distribution
    print("\nCalorie distribution:")
    print(f"  < 150 cal: {len(calories[calories < 150])} recipes")
    print(f"  150-250 cal: {len(calories[(calories >= 150) & (calories < 250)])} recipes")
    print(f"  250-350 cal: {len(calories[(calories >= 250) & (calories < 350)])} recipes")
    print(f"  350-450 cal: {len(calories[(calories >= 350) & (calories < 450)])} recipes")
    print(f"  > 450 cal: {len(calories[calories >= 450])} recipes")
    
    # Show some high-calorie recipes
    high_cal_recipes = df[df['Calories'] >= 300].sort_values('Calories', ascending=False)
    print(f"\nHigh-calorie recipes (>= 300 cal):")
    for _, row in high_cal_recipes.head(10).iterrows():
        print(f"  {row['Dish']}: {row['Calories']} cal")
    
    # Calculate realistic daily totals
    print(f"\nRealistic daily calorie totals:")
    print(f"  3 meals (avg): {calories.mean() * 3:.0f} cal")
    print(f"  3 meals (high): {calories.max() * 3:.0f} cal")
    print(f"  4 meals (avg): {calories.mean() * 4:.0f} cal")
    print(f"  5 meals (avg): {calories.mean() * 5:.0f} cal")

if __name__ == "__main__":
    analyze_calorie_distribution()
