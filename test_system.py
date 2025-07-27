#!/usr/bin/env python3
"""
Test script for Telugu Recipes System
Tests all major components of the application
"""

import sys
import os
from database import RecipeDatabase
from nutrition_api import NutritionAPI
from recipe_processor import RecipeProcessor

def test_database():
    """Test database operations"""
    print("🧪 Testing Database...")
    try:
        db = RecipeDatabase()
        print("✅ Database initialized successfully")
        
        # Test adding a recipe
        recipe_id = db.add_recipe(
            name="Test Recipe",
            ingredients=["1 cup rice", "1 tbsp oil"],
            instructions="Test instructions",
            cooking_time=10,
            difficulty="Easy"
        )
        print(f"✅ Recipe added with ID: {recipe_id}")
        
        # Test getting recipes
        recipes = db.get_all_recipes()
        print(f"✅ Retrieved {len(recipes)} recipes")
        
        # Test search
        search_results = db.search_recipes("rice")
        print(f"✅ Search found {len(search_results)} recipes with 'rice'")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_nutrition_api():
    """Test nutrition API"""
    print("\n🧪 Testing Nutrition API...")
    try:
        api = NutritionAPI()
        ingredients = ["2 cups rice", "1 tbsp oil", "1 tsp turmeric"]
        nutrition = api.get_nutrition_data(ingredients)
        
        print("✅ Nutrition data calculated:")
        for key, value in nutrition.items():
            print(f"   {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Nutrition API test failed: {e}")
        return False

def test_recipe_processor():
    """Test recipe processor"""
    print("\n🧪 Testing Recipe Processor...")
    try:
        processor = RecipeProcessor()
        
        # Test ingredient extraction
        text = "Ingredients: 2 cups rice, 1 tbsp oil, 1 tsp turmeric"
        ingredients = processor.extract_ingredients_from_text(text)
        print(f"✅ Extracted {len(ingredients)} ingredients from text")
        
        # Test recipe parsing
        recipe_text = """
        Test Recipe
        Ingredients:
        2 cups rice
        1 tbsp oil
        Instructions:
        1. Cook rice
        2. Add oil
        """
        parsed = processor.parse_recipe_text(recipe_text)
        print(f"✅ Parsed recipe: {parsed['name']}")
        print(f"   Ingredients: {len(parsed['ingredients'])}")
        
        return True
    except Exception as e:
        print(f"❌ Recipe processor test failed: {e}")
        return False

def test_sample_recipes():
    """Test adding sample recipes"""
    print("\n🧪 Testing Sample Recipes...")
    try:
        processor = RecipeProcessor()
        processor.process_pulihora_recipes()
        print("✅ Sample recipes added successfully")
        return True
    except Exception as e:
        print(f"❌ Sample recipes test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Telugu Recipes System Tests")
    print("=" * 50)
    
    tests = [
        test_database,
        test_nutrition_api,
        test_recipe_processor,
        test_sample_recipes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Run 'python run.py' to start the web application")
        print("   2. Open http://localhost:5000 in your browser")
        print("   3. Click 'Initialize' to add sample recipes")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 