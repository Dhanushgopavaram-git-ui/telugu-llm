# Set page configuration FIRST - before any other Streamlit commands
import streamlit as st

st.set_page_config(
    page_title="తెలుగు ఆహార సలహాదారు | Telugu Diet Assistant",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import json
import os
import sqlite3
import base64
import random
import time
from streamlit_rag_app import get_display_text
from datetime import datetime, timedelta
from database import RecipeDatabase
from nutrition_api import NutritionAPI
from diet_generator import TeluguDietGenerator
from streamlit_rag_app import get_download_link

class CalorieAwareMealPlanner:
    """Enhanced meal planner with calorie-based selection and variety"""

    def __init__(self):
        self.diet_generator = TeluguDietGenerator()

    def load_non_veg_recipes(self):
        """Load only non-vegetarian recipes from CSV"""
        return self.diet_generator._load_non_veg_recipes()

    def load_veg_recipes(self):
        """Load only vegetarian recipes from CSV"""
        return self.diet_generator._load_veg_recipes()

    def load_recipes_by_type(self, diet_type):
        """Load recipes based on diet type"""
        if diet_type == 'vegetarian':
            return self.load_veg_recipes()
        else:
            return self.load_non_veg_recipes()

    def filter_recipes_by_calories(self, recipes, target_calories_per_meal, tolerance=150):
        """Filter recipes that fit within calorie range for a meal - with generous tolerance"""
        # Start with a generous tolerance to ensure variety
        min_calories = max(50, target_calories_per_meal - tolerance)
        max_calories = target_calories_per_meal + tolerance

        filtered = [r for r in recipes if
                   min_calories <= r['nutrition']['calories'] <= max_calories]

        # If no recipes in range, be even more generous
        if not filtered:
            tolerance = 300
            min_calories = max(50, target_calories_per_meal - tolerance)
            max_calories = target_calories_per_meal + tolerance
            filtered = [r for r in recipes if
                       min_calories <= r['nutrition']['calories'] <= max_calories]

        # If still no recipes, return all recipes (no calorie restriction)
        if not filtered:
            print(f"Warning: No recipes found for target {target_calories_per_meal} cal, using all recipes")
            filtered = recipes

        return filtered

    def generate_varied_meal_plan(self, total_calories, meals_per_day=3, days=7, diet_type='non_vegetarian'):
        """Generate a varied meal plan with enhanced variety across all recipes"""
        # Enhanced randomization with multiple entropy sources
        import hashlib
        entropy_string = f"{time.time()}_{random.random()}_{total_calories}_{meals_per_day}_{diet_type}"
        seed_hash = hashlib.md5(entropy_string.encode()).hexdigest()
        seed_value = int(seed_hash[:8], 16) % 100000
        random.seed(seed_value)

        # Load recipes based on diet type
        all_recipes = self.load_recipes_by_type(diet_type)

        if not all_recipes:
            return None

        # Calculate realistic calorie limits based on available recipes
        recipe_calories = [r['nutrition']['calories'] for r in all_recipes]
        max_recipe_calories = max(recipe_calories)
        avg_recipe_calories = sum(recipe_calories) / len(recipe_calories)

        # Adjust target calories to be realistic
        max_possible_daily = max_recipe_calories * meals_per_day
        if total_calories > max_possible_daily:
            print(f"Warning: Target {total_calories} cal exceeds maximum possible {max_possible_daily} cal")
            print(f"Adjusting to realistic target based on available recipes")
            total_calories = min(total_calories, max_possible_daily)

        # Create a global recipe usage tracker to ensure variety across all recipes
        global_used_recipes = set()
        recipe_usage_count = {recipe['id']: 0 for recipe in all_recipes}

        # Calculate calorie distribution
        if meals_per_day == 3:
            # Breakfast: 25%, Lunch: 40%, Dinner: 35%
            calorie_distribution = [0.25, 0.40, 0.35]
            meal_types = ['breakfast', 'lunch', 'dinner']
        elif meals_per_day == 4:
            # Breakfast: 20%, Lunch: 35%, Snack: 15%, Dinner: 30%
            calorie_distribution = [0.20, 0.35, 0.15, 0.30]
            meal_types = ['breakfast', 'lunch', 'snack', 'dinner']
        else:  # 5 meals
            # Breakfast: 20%, Mid-morning: 10%, Lunch: 30%, Evening: 15%, Dinner: 25%
            calorie_distribution = [0.20, 0.10, 0.30, 0.15, 0.25]
            meal_types = ['breakfast', 'mid_morning', 'lunch', 'evening_snack', 'dinner']

        meal_plan = {}
        used_recipe_ids = set()

        for day in range(1, days + 1):
            date = datetime.now() + timedelta(days=day-1)
            day_key = date.strftime('%Y-%m-%d')

            meal_plan[day_key] = {
                'day': day,
                'date': date.strftime('%A, %B %d'),
                'meals': {}
            }

            daily_used_ids = set()

            for i, meal_type in enumerate(meal_types):
                target_calories = int(total_calories * calorie_distribution[i])

                # Filter recipes by calorie target
                suitable_recipes = self.filter_recipes_by_calories(all_recipes, target_calories)

                # Enhanced selection logic for better variety
                # 1. First priority: unused recipes that fit calorie target
                unused_suitable = [r for r in suitable_recipes if r['id'] not in used_recipe_ids]

                # 2. Second priority: recipes not used today that fit calorie target
                daily_unused_suitable = [r for r in suitable_recipes if r['id'] not in daily_used_ids]

                # 3. Third priority: least used recipes that fit calorie target
                if not unused_suitable and not daily_unused_suitable:
                    # Sort by usage count (ascending) to prefer least used recipes
                    suitable_recipes.sort(key=lambda r: recipe_usage_count.get(r['id'], 0))
                    available_recipes = suitable_recipes[:10]  # Top 10 least used
                elif unused_suitable:
                    available_recipes = unused_suitable
                else:
                    available_recipes = daily_unused_suitable

                # Select random recipe from available options
                if available_recipes:
                    selected_recipe = random.choice(available_recipes)
                    meal_plan[day_key]['meals'][meal_type] = selected_recipe
                    daily_used_ids.add(selected_recipe['id'])
                    used_recipe_ids.add(selected_recipe['id'])
                    recipe_usage_count[selected_recipe['id']] += 1
                else:
                    # Fallback: select any recipe if filtering fails
                    if all_recipes:
                        selected_recipe = random.choice(all_recipes)
                        meal_plan[day_key]['meals'][meal_type] = selected_recipe
                        daily_used_ids.add(selected_recipe['id'])
                        used_recipe_ids.add(selected_recipe['id'])
                        recipe_usage_count[selected_recipe['id']] += 1

        return meal_plan

def create_meal_table(meal_plan):
    """Create a structured table from meal plan"""
    table_data = []

    for day_key, day_data in meal_plan.items():
        for meal_type, meal in day_data['meals'].items():
            if meal:
                # Format ingredients as a string
                ingredients_str = ', '.join(meal['ingredients'][:3])  # Show first 3 ingredients
                if len(meal['ingredients']) > 3:
                    ingredients_str += '...'

                # Truncate preparation for table display
                preparation = meal.get('preparation', 'N/A')
                if len(preparation) > 100:
                    preparation = preparation[:100] + '...'

                table_data.append({
                    'Day': f"Day {day_data['day']}",
                    'Meal Type': meal_type.title(),
                    'Dish': meal['name'],
                    'Ingredients': ingredients_str,
                    'Calories': meal['nutrition']['calories'],
                    'Protein_g': meal['nutrition']['protein'],
                    'Carbs_g': meal['nutrition']['carbs'],
                    'Fat_g': meal['nutrition']['fat'],
                    'Fiber_g': meal['nutrition']['fiber'],
                    'Preparation': preparation
                })

    return pd.DataFrame(table_data)

def main():
    try:
        # Instantiate enhanced meal planner
        meal_planner = CalorieAwareMealPlanner()

        # Sidebar for language selection
        with st.sidebar:
            st.title("🌐 భాష / Language")
            lang = st.radio(
                "Select your preferred language:",
                ["తెలుగు (Telugu)", "English"],
                index=0
            )
            selected_lang = 'telugu' if lang == "తెలుగు (Telugu)" else 'english'

        # Main title
        st.title(get_display_text('title', selected_lang))
        st.subheader(get_display_text('subtitle', selected_lang))

        # Sidebar inputs
        with st.sidebar:
            st.header(get_display_text('goal_label', selected_lang))
            goal = st.selectbox(
                "",
                [
                    get_display_text('weight_loss', selected_lang),
                    get_display_text('weight_gain', selected_lang),
                    get_display_text('diabetes', selected_lang),
                    get_display_text('energy', selected_lang)
                ]
            )

            st.header(get_display_text('diet_type_label', selected_lang))
            diet_type = st.radio(
                "",
                [
                    get_display_text('veg', selected_lang),
                    get_display_text('non_veg', selected_lang)
                ]
            )

            st.header(get_display_text('meals_label', selected_lang))
            meals_per_day = st.slider("", 3, 5, 3)

            st.header(get_display_text('calories_label', selected_lang))
            calorie_limit = st.slider("", 1200, 3000, 2000, 100)

            # Show realistic calorie info based on diet type
            if diet_type == get_display_text('veg', 'telugu') or diet_type == get_display_text('veg', 'english'):
                st.info("ℹ️ Note: Vegetarian recipes range 210-416 cal each. Realistic daily totals: 630-1248 calories for 3 meals.")
            else:
                st.info("ℹ️ Note: Non-vegetarian recipes range 110-330 cal each. Realistic daily totals: 330-990 calories for 3 meals.")

            st.header(get_display_text('allergies_label', selected_lang))
            allergies = st.text_input("")

        # Generate button
        if st.button(get_display_text('generate_button', selected_lang), type="primary"):
            # Map UI selections to diet generator preferences
            health_goal_map = {
                get_display_text('weight_loss', 'telugu'): 'weight_loss',
                get_display_text('weight_loss', 'english'): 'weight_loss',
                get_display_text('weight_gain', 'telugu'): 'weight_gain',
                get_display_text('weight_gain', 'english'): 'weight_gain',
                get_display_text('diabetes', 'telugu'): 'diabetic',
                get_display_text('diabetes', 'english'): 'diabetic',
                get_display_text('energy', 'telugu'): 'energy_boost',
                get_display_text('energy', 'english'): 'energy_boost'
            }

            diet_type_map = {
                get_display_text('veg', 'telugu'): 'vegetarian',
                get_display_text('veg', 'english'): 'vegetarian',
                get_display_text('non_veg', 'telugu'): 'non_vegetarian',
                get_display_text('non_veg', 'english'): 'non_vegetarian'
            }

            # Debug: Show what's being mapped
            st.write(f"Debug - Goal selected: {goal}")
            st.write(f"Debug - Diet type selected: {diet_type}")
            st.write(f"Debug - Mapped goal: {health_goal_map.get(goal, 'energy_boost')}")
            st.write(f"Debug - Mapped diet type: {diet_type_map.get(diet_type, 'vegetarian')}")

            # Create user input string for diet generator
            mapped_goal = health_goal_map.get(goal, 'energy_boost')
            mapped_diet_type = diet_type_map.get(diet_type, 'vegetarian')
            user_input = f"{mapped_goal} {mapped_diet_type} {meals_per_day} meals {calorie_limit} calories"
            if allergies:
                user_input += f" allergies: {allergies}"

            st.write(f"Debug - Final user input: {user_input}")

            with st.spinner('Generating your personalized diet plan...'):
                # Generate calorie-aware meal plan based on selected diet type
                meal_plan_data = meal_planner.generate_varied_meal_plan(
                    total_calories=calorie_limit,
                    meals_per_day=meals_per_day,
                    days=7,
                    diet_type=mapped_diet_type
                )

                if meal_plan_data:
                    # Create structured table
                    meal_table = create_meal_table(meal_plan_data)

                    # Calculate nutrition summary
                    total_calories = meal_table['Calories'].sum()
                    total_protein = meal_table['Protein_g'].sum()
                    total_carbs = meal_table['Carbs_g'].sum()
                    total_fat = meal_table['Fat_g'].sum()
                    total_fiber = meal_table['Fiber_g'].sum()

                    days_count = len(meal_plan_data)

                    nutrition_summary = {
                        'avg_calories_per_day': round(total_calories / days_count, 1),
                        'avg_protein_per_day': round(total_protein / days_count, 1),
                        'avg_carbs_per_day': round(total_carbs / days_count, 1),
                        'avg_fat_per_day': round(total_fat / days_count, 1),
                        'avg_fiber_per_day': round(total_fiber / days_count, 1),
                        'calories': round(total_calories / (days_count * meals_per_day), 1),
                        'protein': round(total_protein / (days_count * meals_per_day), 1),
                        'carbs': round(total_carbs / (days_count * meals_per_day), 1),
                        'fat': round(total_fat / (days_count * meals_per_day), 1),
                        'fiber': round(total_fiber / (days_count * meals_per_day), 1)
                    }

                    # Generate Telugu recommendations
                    recommendations = meal_planner.diet_generator._generate_telugu_recommendations({
                        'health_goal': mapped_goal,
                        'diet_type': 'non_vegetarian',
                        'calorie_limit': calorie_limit
                    })

                    diet_plan = {
                        'meal_plan': meal_plan_data,
                        'meal_table': meal_table,
                        'nutrition_summary': nutrition_summary,
                        'recommendations': recommendations
                    }

                    # Store in session state
                    st.session_state.diet_plan = diet_plan
                    st.session_state.selected_lang = selected_lang
                else:
                    st.error("Could not generate meal plan. Please try again.")

        # Display diet plan if available
        if hasattr(st.session_state, 'diet_plan'):
            diet_plan = st.session_state.diet_plan
            selected_lang = st.session_state.selected_lang

            if not diet_plan or not diet_plan.get('meal_plan') or len(diet_plan['meal_plan']) == 0:
                st.warning("No diet menu could be generated. Please check your recipe data or try different options.")
                st.write("Debug: diet_plan output:")
                st.write(diet_plan)
            else:
                # Create tabs
                tab1, tab2, tab3 = st.tabs([
                    get_display_text('plan_tab', selected_lang),
                    get_display_text('nutrition_tab', selected_lang),
                    get_display_text('recommendations_tab', selected_lang)
                ])

                # Tab 1: Diet Plan - Structured Table View
                with tab1:
                    st.subheader("📋 Complete Meal Plan (Non-Vegetarian Only)")

                    # Display the structured table
                    if 'meal_table' in diet_plan:
                        st.dataframe(
                            diet_plan['meal_table'],
                            use_container_width=True,
                            hide_index=True
                        )

                        # Add expandable sections for detailed preparation
                        st.subheader("🍳 Detailed Preparation Instructions")

                        # Group by day for better organization
                        for day_key, day_data in diet_plan['meal_plan'].items():
                            with st.expander(f"Day {day_data['day']} - {day_data['date']}"):
                                for meal_type, meal in day_data['meals'].items():
                                    if meal:
                                        st.markdown(f"### {meal_type.title()}: {meal['name']}")

                                        # Ingredients
                                        st.markdown("**Ingredients:**")
                                        ingredients_text = ""
                                        if isinstance(meal['ingredients'], list):
                                            ingredients_text = ", ".join(meal['ingredients'])
                                        else:
                                            ingredients_text = str(meal['ingredients'])
                                        st.markdown(ingredients_text)

                                        # Nutrition info in columns
                                        col1, col2, col3, col4, col5 = st.columns(5)
                                        with col1:
                                            st.metric("Calories", meal['nutrition']['calories'])
                                        with col2:
                                            st.metric("Protein", f"{meal['nutrition']['protein']}g")
                                        with col3:
                                            st.metric("Carbs", f"{meal['nutrition']['carbs']}g")
                                        with col4:
                                            st.metric("Fat", f"{meal['nutrition']['fat']}g")
                                        with col5:
                                            st.metric("Fiber", f"{meal['nutrition']['fiber']}g")

                                        # Full preparation instructions
                                        st.markdown("**Preparation:**")
                                        st.markdown(meal.get('preparation', 'N/A'))
                                        st.markdown("---")

                    # Download button
                    if 'meal_table' in diet_plan:
                        csv = diet_plan['meal_table'].to_csv(index=False)
                        st.download_button(
                            label="📥 Download Meal Plan as CSV",
                            data=csv,
                            file_name=f"telugu_diet_plan_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

                # Tab 2: Nutrition Information
                with tab2:
                    nutrition_summary = diet_plan.get('nutrition_summary', {})

                    # Daily nutrition overview
                    st.subheader("📊 Daily Nutrition Summary")

                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric(
                            "Daily Calories",
                            f"{nutrition_summary.get('avg_calories_per_day', 0):.0f}",
                            f"Target: {calorie_limit}"
                        )
                    with col2:
                        st.metric("Daily Protein", f"{nutrition_summary.get('avg_protein_per_day', 0):.1f}g")
                    with col3:
                        st.metric("Daily Carbs", f"{nutrition_summary.get('avg_carbs_per_day', 0):.1f}g")
                    with col4:
                        st.metric("Daily Fat", f"{nutrition_summary.get('avg_fat_per_day', 0):.1f}g")
                    with col5:
                        st.metric("Daily Fiber", f"{nutrition_summary.get('avg_fiber_per_day', 0):.1f}g")

                    # Nutrition breakdown chart
                    st.subheader("📈 Nutrition Breakdown")

                    # Create nutrition breakdown data
                    nutrition_chart_data = pd.DataFrame({
                        'Nutrient': ['Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Fiber (g)'],
                        'Daily Average': [
                            nutrition_summary.get('avg_calories_per_day', 0),
                            nutrition_summary.get('avg_protein_per_day', 0),
                            nutrition_summary.get('avg_carbs_per_day', 0),
                            nutrition_summary.get('avg_fat_per_day', 0),
                            nutrition_summary.get('avg_fiber_per_day', 0)
                        ]
                    })

                    st.bar_chart(nutrition_chart_data.set_index('Nutrient'))

                    # Calorie distribution by meal type
                    if 'meal_table' in diet_plan:
                        st.subheader("🍽️ Calorie Distribution by Meal Type")
                        meal_calories = diet_plan['meal_table'].groupby('Meal Type')['Calories'].mean()
                        st.bar_chart(meal_calories)

                # Tab 3: Recommendations
                with tab3:
                    for rec in diet_plan['recommendations']:
                        st.markdown(f"- {rec}")

        # Always show something if nothing rendered
        if not st.session_state.get('diet_plan'):
            st.info("No diet plan generated yet. Please select your options and click Generate Diet Plan.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        import traceback
        st.text(traceback.format_exc())

if __name__ == "__main__":
    main()
