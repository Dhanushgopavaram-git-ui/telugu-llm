import streamlit as st
import pandas as pd
import json
import os
import base64
from datetime import datetime, timedelta
from database import RecipeDatabase
from nutrition_api import NutritionAPI
from rag_system import TeluguDietRAG
import time

# Initialize components
db = RecipeDatabase()
nutrition_api = NutritionAPI()

# Initialize RAG system
@st.cache_resource
def load_rag_system():
    # Get OpenAI API key from environment or user input
    openai_api_key = os.environ.get('OPENAI_API_KEY', None)
    if not openai_api_key:
        # Will be handled in the UI
        pass
    
    return TeluguDietRAG(openai_api_key=openai_api_key)

try:
    rag_system = load_rag_system()
except Exception as e:
    st.error(f"Error loading RAG system: {e}")
    rag_system = None

# Set page configuration
st.set_page_config(
    page_title="తెలుగు ఆహార సలహాదారు | Telugu Diet Assistant",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to toggle language
def get_display_text(key, lang='telugu'):
    text_dict = {
        'title': {
            'telugu': 'తెలుగు సాంప్రదాయ ఆహార సలహాదారు',
            'english': 'Telugu Traditional Diet Assistant'
        },
        'subtitle': {
            'telugu': 'మీ ఆరోగ్య లక్ష్యాలకు అనుగుణంగా సాంప్రదాయ తెలుగు ఆహార ప్రణాళికలు',
            'english': 'Personalized traditional Telugu diet plans for your health goals'
        },
        'goal_label': {
            'telugu': 'మీ ఆహార లక్ష్యం ఎంచుకోండి:',
            'english': 'Select your dietary goal:'
        },
        'weight_loss': {
            'telugu': 'బరువు తగ్గాలి',
            'english': 'Weight Loss'
        },
        'weight_gain': {
            'telugu': 'బరువు పెరగాలి',
            'english': 'Weight Gain'
        },
        'diabetes': {
            'telugu': 'మధుమేహం',
            'english': 'Diabetes Friendly'
        },
        'energy': {
            'telugu': 'శక్తివంతమైన ఆహారం',
            'english': 'High-Energy'
        },
        'diet_type_label': {
            'telugu': 'ఆహార రకం:',
            'english': 'Diet Type:'
        },
        'veg': {
            'telugu': 'శాకాహారం',
            'english': 'Vegetarian'
        },
        'non_veg': {
            'telugu': 'మాంసాహారం',
            'english': 'Non-Vegetarian'
        },
        'meals_label': {
            'telugu': 'రోజుకు ఎన్ని భోజనాలు కావాలి:',
            'english': 'Meals per day:'
        },
        'calories_label': {
            'telugu': 'రోజుకు గరిష్ట కాలరీ పరిమితి:',
            'english': 'Daily Calorie Limit:'
        },
        'allergies_label': {
            'telugu': 'అలర్జీలు లేదా తినదగని పదార్థాలు:',
            'english': 'Allergies or exclusions:'
        },
        'generate_button': {
            'telugu': 'ఆహార ప్రణాళిక తయారు చేయండి',
            'english': 'Generate Diet Plan'
        },
        'plan_tab': {
            'telugu': 'ఆహార ప్రణాళిక',
            'english': 'Diet Plan'
        },
        'nutrition_tab': {
            'telugu': 'పోషకాల సమాచారం',
            'english': 'Nutritional Information'
        },
        'recommendations_tab': {
            'telugu': 'సిఫార్సులు',
            'english': 'Recommendations'
        },
        'download_button': {
            'telugu': 'ఆహార ప్రణాళిక డౌన్‌లోడ్ చేయండి',
            'english': 'Download Diet Plan'
        },
        'breakfast': {
            'telugu': 'అల్పాహారం',
            'english': 'Breakfast'
        },
        'lunch': {
            'telugu': 'మధ్యాహ్న భోజనం',
            'english': 'Lunch'
        },
        'dinner': {
            'telugu': 'రాత్రి భోజనం',
            'english': 'Dinner'
        },
        'snack': {
            'telugu': 'చిరుతిండి',
            'english': 'Snack'
        },
        'calories': {
            'telugu': 'కేలరీలు',
            'english': 'Calories'
        },
        'protein': {
            'telugu': 'ప్రోటీన్',
            'english': 'Protein'
        },
        'carbs': {
            'telugu': 'కార్బోహైడ్రేట్స్',
            'english': 'Carbs'
        },
        'fat': {
            'telugu': 'కొవ్వు',
            'english': 'Fat'
        },
        'fiber': {
            'telugu': 'ఫైబర్',
            'english': 'Fiber'
        },
        'day': {
            'telugu': 'రోజు',
            'english': 'Day'
        },
        'daily_average': {
            'telugu': 'రోజువారీ సగటు పోషకాలు',
            'english': 'Daily Average Nutrition'
        },
        'ask_question_label': {
            'telugu': 'మీ ఆహార ప్రశ్న అడగండి:',
            'english': 'Ask your diet question:'
        },
        'ask_button': {
            'telugu': 'ప్రశ్న అడగండి',
            'english': 'Ask Question'
        },
        'api_key_label': {
            'telugu': 'OpenAI API కీ:',
            'english': 'OpenAI API Key:'
        },
        'save_key_button': {
            'telugu': 'API కీ సేవ్ చేయండి',
            'english': 'Save API Key'
        },
        'api_key_info': {
            'telugu': 'మెరుగైన సిఫార్సుల కోసం OpenAI API కీని ఉపయోగించండి',
            'english': 'Use OpenAI API key for better recommendations'
        }
    }
    
    return text_dict.get(key, {}).get(lang, key)

# Function to create a downloadable link for the diet plan
def get_download_link(diet_plan, lang):
    now = datetime.now().strftime("%Y-%m-%d")
    filename = f"telugu_diet_plan_{now}.txt"
    content = generate_diet_plan_text(diet_plan, lang)
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Click here to download</a>'

# Function to generate text content for the diet plan
def generate_diet_plan_text(diet_plan, lang):
    content = []
    
    # Add title
    if lang == 'telugu':
        content.append("తెలుగు సాంప్రదాయ ఆహార ప్రణాళిక")
        content.append("=================================\n")
    else:
        content.append("Telugu Traditional Diet Plan")
        content.append("=================================\n")
    
    # Add preferences
    if lang == 'telugu':
        content.append(f"ఆహార లక్ష్యం: {get_display_text(diet_plan['preferences']['health_goal'], 'telugu')}")
        content.append(f"ఆహార రకం: {get_display_text(diet_plan['preferences']['diet_type'], 'telugu')}")
        content.append(f"రోజుకు కేలరీలు: {diet_plan['preferences']['calorie_target']}\n")
    else:
        content.append(f"Dietary Goal: {get_display_text(diet_plan['preferences']['health_goal'], 'english')}")
        content.append(f"Diet Type: {get_display_text(diet_plan['preferences']['diet_type'], 'english')}")
        content.append(f"Daily Calories: {diet_plan['preferences']['calorie_target']}\n")
    
    # Add meal plan
    for day, day_data in diet_plan['meal_plan'].items():
        if lang == 'telugu':
            content.append(f"రోజు {day_data['day']}: {day_data['telugu_date']}")
            content.append("----------------------------------")
        else:
            content.append(f"Day {day_data['day']}: {day_data['date']}")
            content.append("----------------------------------")
        
        for meal_type, meal in day_data['meals'].items():
            if meal:
                meal_name = get_display_text(meal_type, lang)
                content.append(f"{meal_name}: {meal['name']}")
                
                if lang == 'telugu':
                    content.append(f"  కేలరీలు: {meal['nutrition'].get('calories', 0)}")
                    content.append(f"  ప్రోటీన్: {meal['nutrition'].get('protein', 0)}g")
                else:
                    content.append(f"  Calories: {meal['nutrition'].get('calories', 0)}")
                    content.append(f"  Protein: {meal['nutrition'].get('protein', 0)}g")
        
        content.append("")
    
    # Add recommendations
    if lang == 'telugu':
        content.append("సిఫార్సులు:")
        content.append("----------------------------------")
    else:
        content.append("Recommendations:")
        content.append("----------------------------------")
    
    for rec in diet_plan['recommendations']:
        content.append(f"- {rec}")
    
    return "\n".join(content)

# Function to generate PDF of the diet plan
def generate_pdf(diet_plan, lang):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create content
        content = []
        
        # Title
        title_text = "తెలుగు సాంప్రదాయ ఆహార ప్రణాళిక" if lang == 'telugu' else "Telugu Traditional Diet Plan"
        title = Paragraph(title_text, styles['Title'])
        content.append(title)
        content.append(Spacer(1, 12))
        
        # Preferences
        pref_text = []
        if lang == 'telugu':
            pref_text.append(f"ఆహార లక్ష్యం: {get_display_text(diet_plan['preferences']['health_goal'], 'telugu')}")
            pref_text.append(f"ఆహార రకం: {get_display_text(diet_plan['preferences']['diet_type'], 'telugu')}")
            pref_text.append(f"రోజుకు కేలరీలు: {diet_plan['preferences']['calorie_target']}")
        else:
            pref_text.append(f"Dietary Goal: {get_display_text(diet_plan['preferences']['health_goal'], 'english')}")
            pref_text.append(f"Diet Type: {get_display_text(diet_plan['preferences']['diet_type'], 'english')}")
            pref_text.append(f"Daily Calories: {diet_plan['preferences']['calorie_target']}")
        
        for text in pref_text:
            p = Paragraph(text, styles['Normal'])
            content.append(p)
        
        content.append(Spacer(1, 12))
        
        # Meal plan
        for day, day_data in diet_plan['meal_plan'].items():
            day_title = f"రోజు {day_data['day']}: {day_data['telugu_date']}" if lang == 'telugu' else f"Day {day_data['day']}: {day_data['date']}"
            day_heading = Paragraph(day_title, styles['Heading2'])
            content.append(day_heading)
            
            for meal_type, meal in day_data['meals'].items():
                if meal:
                    meal_name = get_display_text(meal_type, lang)
                    meal_text = f"{meal_name}: {meal['name']}"
                    p = Paragraph(meal_text, styles['Normal'])
                    content.append(p)
                    
                    nutrition_text = ""
                    if lang == 'telugu':
                        nutrition_text = f"కేలరీలు: {meal['nutrition'].get('calories', 0)}, ప్రోటీన్: {meal['nutrition'].get('protein', 0)}g"
                    else:
                        nutrition_text = f"Calories: {meal['nutrition'].get('calories', 0)}, Protein: {meal['nutrition'].get('protein', 0)}g"
                    
                    p = Paragraph(nutrition_text, styles['Normal'])
                    content.append(p)
            
            content.append(Spacer(1, 12))
        
        # Recommendations
        rec_title = "సిఫార్సులు:" if lang == 'telugu' else "Recommendations:"
        rec_heading = Paragraph(rec_title, styles['Heading2'])
        content.append(rec_heading)
        
        for rec in diet_plan['recommendations']:
            p = Paragraph(f"• {rec}", styles['Normal'])
            content.append(p)
        
        # Build PDF
        doc.build(content)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# Main app
def main():
    # Sidebar for language selection
    with st.sidebar:
        st.title("🌐 భాష / Language")
        lang = st.radio(
            "Select your preferred language:",
            ["తెలుగు (Telugu)", "English"],
            index=0
        )
        
        selected_lang = 'telugu' if lang == "తెలుగు (Telugu)" else 'english'
        
        # OpenAI API Key input
        st.markdown("---")
        st.subheader(get_display_text('api_key_label', selected_lang))
        st.caption(get_display_text('api_key_info', selected_lang))
        
        api_key = st.text_input("", type="password")
        if st.button(get_display_text('save_key_button', selected_lang)):
            if api_key:
                os.environ['OPENAI_API_KEY'] = api_key
                st.success("API key saved!")
                st.rerun()
    
    # Main title
    st.title(get_display_text('title', selected_lang))
    st.subheader(get_display_text('subtitle', selected_lang))
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Diet Plan Generator", "Ask Diet Questions"])
    
    # Tab 1: Diet Plan Generator
    with tab1:
        # Sidebar inputs
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
        
        st.header(get_display_text('allergies_label', selected_lang))
        allergies = st.text_input("", key="allergies_input")
        
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
            
            # Create user input string for diet generator
            user_input = f"{health_goal_map.get(goal, 'energy_boost')} {diet_type_map.get(diet_type, 'vegetarian')} {meals_per_day} meals {calorie_limit} calories"
            if allergies:
                user_input += f" allergies: {allergies}"
            
            with st.spinner('Generating your personalized diet plan...'):
                # Use RAG system if available, otherwise fallback to regular diet generator
                if rag_system is not None:
                    diet_plan = rag_system.generate_diet_plan(user_input, selected_lang)
                else:
                    from diet_generator import TeluguDietGenerator
                    diet_generator = TeluguDietGenerator()
                    diet_plan = diet_generator.generate_diet_menu(user_input)
                
                # Store in session state
                st.session_state.diet_plan = diet_plan
                st.session_state.selected_lang = selected_lang
        
        # Display diet plan if available
        if hasattr(st.session_state, 'diet_plan'):
            diet_plan = st.session_state.diet_plan
            selected_lang = st.session_state.selected_lang
            
            # Create tabs for diet plan display
            plan_tab, nutrition_tab, rec_tab = st.tabs([
                get_display_text('plan_tab', selected_lang),
                get_display_text('nutrition_tab', selected_lang),
                get_display_text('recommendations_tab', selected_lang)
            ])
            
            # Tab 1: Diet Plan
            with plan_tab:
                for day, day_data in diet_plan['meal_plan'].items():
                    st.subheader(f"{get_display_text('day', selected_lang)} {day_data['day']}: {day_data['telugu_date'] if selected_lang == 'telugu' else day_data['date']}")
                    
                    cols = st.columns(len(day_data['meals']))
                    for i, (meal_type, meal) in enumerate(day_data['meals'].items()):
                        if meal:
                            with cols[i]:
                                st.markdown(f"**{get_display_text(meal_type, selected_lang)}**")
                                st.markdown(f"**{meal['name']}**")
                                
                                # Display ingredients
                                if 'ingredients' in meal:
                                    st.markdown("**Ingredients:**")
                                    for ingredient in meal['ingredients'][:5]:  # Show first 5 ingredients
                                        st.markdown(f"- {ingredient}")
                                    if len(meal['ingredients']) > 5:
                                        st.markdown("...")
                                
                                # Display nutrition info
                                st.markdown(f"**{get_display_text('calories', selected_lang)}:** {meal['nutrition'].get('calories', 0)}")
                                st.markdown(f"**{get_display_text('protein', selected_lang)}:** {meal['nutrition'].get('protein', 0)}g")
                    st.markdown("---")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(get_download_link(diet_plan, selected_lang), unsafe_allow_html=True)
                
                with col2:
                    # PDF download button
                    pdf_data = generate_pdf(diet_plan, selected_lang)
                    if pdf_data:
                        now = datetime.now().strftime("%Y-%m-%d")
                        filename = f"telugu_diet_plan_{now}.pdf"
                        st.download_button(
                            label="Download as PDF",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf"
                        )
            
            # Tab 2: Nutrition Information
            with nutrition_tab:
                # Create nutrition summary dataframe
                nutrition_data = {
                    get_display_text('calories', selected_lang): [diet_plan['nutrition_summary']['calories']],
                    get_display_text('protein', selected_lang) + " (g)": [diet_plan['nutrition_summary']['protein']],
                    get_display_text('carbs', selected_lang) + " (g)": [diet_plan['nutrition_summary']['carbs']],
                    get_display_text('fat', selected_lang) + " (g)": [diet_plan['nutrition_summary']['fat']],
                    get_display_text('fiber', selected_lang) + " (g)": [diet_plan['nutrition_summary']['fiber']]
                }
                
                nutrition_df = pd.DataFrame(nutrition_data)
                st.subheader(get_display_text('daily_average', selected_lang))
                st.dataframe(nutrition_df)
                
                # Create a bar chart
                st.bar_chart(nutrition_df.iloc[0])
            
            # Tab 3: Recommendations
            with rec_tab:
                for rec in diet_plan['recommendations']:
                    st.markdown(f"- {rec}")
    
    # Tab 2: Ask Diet Questions
    with tab2:
        st.header(get_display_text('ask_question_label', selected_lang))
        question = st.text_input("", key="question_input")
        
        if st.button(get_display_text('ask_button', selected_lang), type="primary"):
            if not question:
                st.warning("Please enter a question")
            elif rag_system is None:
                st.error("RAG system is not available. Please check your dependencies or provide an OpenAI API key.")
            else:
                with st.spinner('Searching for an answer...'):
                    answer = rag_system.answer_nutrition_question(question, selected_lang)
                    st.markdown("### Answer:")
                    st.markdown(answer)

if __name__ == "__main__":
    main()