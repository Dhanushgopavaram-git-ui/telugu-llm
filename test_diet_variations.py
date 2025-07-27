import json
import random
from diet_generator import TeluguDietGenerator

# Set a fixed seed for reproducibility in testing
random.seed(42)

# Create the diet generator
diet_gen = TeluguDietGenerator()

# Test cases with different inputs
test_cases = [
    "I want a vegetarian diet for weight loss",
    "I need a non-veg diet for weight gain",
    "I want a vegetarian diet for diabetic patients",
    "I need a protein-rich diet for muscle building",
    "I want a vegan diet for energy boost"
]

# Run tests and save results
results = {}
for i, test_input in enumerate(test_cases):
    print(f"\nTest Case {i+1}: {test_input}")
    result = diet_gen.generate_diet_menu(test_input)
    
    # Extract just the first day's meal plan for comparison
    first_day_key = list(result['meal_plan'].keys())[0] if result['meal_plan'] else None
    first_day_plan = result['meal_plan'].get(first_day_key, {}) if first_day_key else {}
    
    # Print meal names for the first day
    if 'meals' in first_day_plan:
        print("Meals for first day:")
        for meal_type, meal in first_day_plan['meals'].items():
            if meal:
                print(f"  {meal_type}: {meal.get('name', 'Unknown')}")
            else:
                print(f"  {meal_type}: None")
    
    # Store results for comparison
    results[f"Test {i+1}"] = {
        "input": test_input,
        "preferences": result.get('preferences', {}),
        "first_day_meals": {k: v.get('name') if v else None 
                           for k, v in first_day_plan.get('meals', {}).items()}
    }

# Save results to file for analysis
with open('diet_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nTest completed. Results saved to diet_test_results.json")

# Check if we're getting different meals for different inputs
meal_sets = [set(result['first_day_meals'].values()) for result in results.values()]

# Compare meal sets
all_same = True
for i in range(1, len(meal_sets)):
    if meal_sets[i] != meal_sets[0]:
        all_same = False
        break

print(f"\nAll test cases produced the same meals: {all_same}")
if all_same:
    print("The diet generator is still producing the same meals for different inputs.")
else:
    print("Success! The diet generator is now producing different meals for different inputs.")