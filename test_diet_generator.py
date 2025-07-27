#!/usr/bin/env python3
"""
Test script for Telugu Diet Generator
Tests the AI-powered diet menu generation
"""

from diet_generator import TeluguDietGenerator

def test_diet_generator():
    """Test the diet generator with various inputs"""
    print("🧪 Testing Telugu Diet Generator...")
    
    generator = TeluguDietGenerator()
    
    # Test cases
    test_cases = [
        "vegetarian diet for weight loss, 1500 calories",
        "diabetic diet low sugar for a week",
        "protein rich diet for muscle gain",
        "vegan diet for energy boost",
        "బరువు తగ్గించడానికి శాకాహార ఆహారం",
        "మధుమేహం కోసం తక్కువ చక్కెర ఆహారం"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_input}")
        
        try:
            result = generator.generate_diet_menu(test_input)
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Diet plan generated successfully")
                print(f"   - Duration: {result['preferences']['duration']} days")
                print(f"   - Diet type: {result['preferences']['diet_type']}")
                print(f"   - Health goal: {result['preferences']['health_goal']}")
                print(f"   - Meals per day: {result['preferences']['meals_per_day']}")
                
                if result['nutrition_summary']:
                    print(f"   - Avg calories: {result['nutrition_summary']['calories']}")
                    print(f"   - Avg protein: {result['nutrition_summary']['protein']}g")
                
                if result['meal_plan']:
                    print(f"   - Meal plan days: {len(result['meal_plan'])}")
                
                if result['recommendations']:
                    print(f"   - Recommendations: {len(result['recommendations'])}")
                    for rec in result['recommendations'][:2]:  # Show first 2
                        print(f"     • {rec}")
            
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n🎉 Diet generator test completed!")

def test_diet_suggestions():
    """Test diet suggestions functionality"""
    print("\n🧪 Testing Diet Suggestions...")
    
    generator = TeluguDietGenerator()
    
    test_queries = [
        "breakfast",
        "lunch",
        "dinner",
        "అల్పాహారం",
        "మధ్యాహ్న భోజనం"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        suggestions = generator.get_diet_suggestions(query)
        
        for meal_type, items in suggestions.items():
            if items:
                print(f"   {meal_type}: {len(items)} suggestions")
                for item in items[:2]:  # Show first 2
                    print(f"     • {item}")
    
    print("\n✅ Diet suggestions test completed!")

if __name__ == '__main__':
    test_diet_generator()
    test_diet_suggestions() 