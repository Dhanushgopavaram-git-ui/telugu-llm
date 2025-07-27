# � తెలుగు సాంప్రదాయ ఆహార సలహాదారు (Telugu Traditional Diet Assistant)

A comprehensive web application for managing and discovering authentic Telugu recipes with nutrition information, structured data, and a powerful query interface. Now featuring a Streamlit-based Retrieval-Augmented Generation (RAG) system that functions as a Telugu traditional diet assistant.

---

## ✨ Features

### ✅ What You Have Now

* **Traditional Telugu Recipes**: Authentic Pulihora recipes and more
* **AI-Powered Diet Menu Generator**: LLM that creates personalized Telugu diet plans
* **Nutrition Data**: Automatic nutrition calculation based on ingredients
* **Structured Format**: Organized recipe database with ingredients, instructions, and metadata
* **Query Interface**: Beautiful web interface with search functionality
* **Modern UI**: Responsive design with beautiful gradients and animations
* **Streamlit RAG Application**: Interactive diet assistant with personalized recommendations
* **Language Toggle**: Switch between Telugu and English interfaces
* **Diet Plan Download**: Export your diet plan as text or PDF
* **Diet Q\&A**: Ask questions about Telugu traditional foods and nutrition

### 🔧 Technical Features

* **SQLite Database**: Efficient storage and retrieval of recipes
* **Nutrition API Integration**: Real-time nutrition calculation (with fallback to mock data)
* **Flask Web Framework**: Fast and reliable web application
* **Bootstrap 5**: Modern, responsive UI components
* **RESTful API**: JSON endpoints for programmatic access
* **Streamlit**: Interactive web application for diet planning
* **LangChain**: LLM-powered Q\&A and retrieval from recipe data
* **FAISS/SentenceTransformer**: Vector similarity search for recipe recommendations
* **OpenAI Integration**: Enhanced diet recommendations and Q\&A

---

## 🚀 Quick Start

### Prerequisites

* Python 3.7 or higher
* pip (Python package installer)

### Installation

1. **Clone or download the project files**
2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the following:

```bash
NUTRITION_API_KEY=your_edamam_api_key
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

4. **Run the Flask application (Optional)**

```bash
python app.py
```

Navigate to `http://localhost:5000`

5. **Initialize the database**
   Click the "Initialize" button in the navigation to add sample recipes

6. **Run the Streamlit RAG application**

```bash
streamlit run streamlit_rag_app.py
```

Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```bash
telugu-llm/
├── app.py                     # Main Flask application
├── config.py                  # Configuration settings
├── database.py                # Database operations
├── nutrition_api.py           # Nutrition API integration
├── recipe_processor.py        # Recipe processing utilities
├── diet_generator.py          # Rule-based diet plan generator
├── rag_system.py              # Retrieval-Augmented Generation system
├── streamlit_rag_app.py       # Streamlit application for diet assistant
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── recipe_detail.html
│   ├── add_recipe.html
│   └── search_results.html
└── README.md                  # This file
```

---

## 🌟 Using the Streamlit RAG Application

### Diet Plan Generator

1. Select language preference
2. Enter OpenAI API key (optional)
3. Choose dietary goal (weight loss, weight gain, diabetic, etc.)
4. Choose diet type (vegetarian/non-vegetarian)
5. Specify meals per day and calorie range
6. Enter allergies or exclusions
7. Click "Generate Diet Plan"

### Diet Q\&A

Ask diet-related questions in Telugu or English and receive intelligent answers powered by RAG.

---

## 🍽️ Sample Recipes Included

### Breakfast (అల్పాహారం)

* Idli Sambar
* Dosa Chutney
* Pongal
* Upma
* Puri Aloo Curry
* Pesarattu

### Main Course (ముఖ్య భోజనం)

* Classic Tamarind Pulihora
* Lemon Pulihora
* Coconut Pulihora
* Peanut Pulihora
* Biryani
* Ragi Mudde

### Side Dishes (పక్క వంటకాలు)

* Gongura Pachadi
* Gutti Vankaya

### Snacks (చిరుతిండి)

* Mirchi Bajji
* Bonda

### Desserts (మిఠాయి)

* Pootharekulu
* Gavvalu

---

## 🤖 AI Diet Menu Generator (ఆహార పట్టిక జనరేటర్)

* Accepts natural language input in English or Telugu
* Personalized Telugu diet plans
* Multi-day plans
* Nutrition breakdowns
* Goal-based diet support

**Example Inputs:**

* "vegetarian diet for weight loss, 1500 calories"
* "బరువు తగ్గించడానికి శాకాహార ఆహారం"
* "మధుమేహం కోసం తక్కువ చక్కెర ఆహారం"

---

## 🔍 Advanced Search & Customization

* Filter by category, difficulty, cooking time, nutrition
* Search by ingredients or recipe name
* Real-time results and smart recommendations
* Tag-based filtering and browsing

---

## 📊 Nutrition Information

Each recipe includes:

* Calories
* Protein
* Carbs
* Fat
* Fiber
* Sugar
* Sodium

---

## 🛠️ API Endpoints

* `GET /api/recipes` - Get all recipes
* `GET /api/search?q=` - Search recipes
* `POST /add_recipe` - Add new recipe

---

## 🎨 UI Features

* Responsive Design
* Beautiful Gradients
* Hover Effects & Animations
* Nutrition Charts
* Real-time Previews

---

## 🔧 Configuration

Create a `.env` file for API keys:

```env
NUTRITION_API_KEY=your_key
FLASK_SECRET_KEY=your_secret
```

---

## 📊 Database Schema

### Recipes Table

* id
* name
* ingredients (JSON)
* instructions
* cooking\_time
* difficulty
* cuisine\_type
* created\_at

### Nutrition Table

* id
* recipe\_id
* calories
* protein
* carbs
* fat
* fiber
* sugar
* sodium

---

## 🚀 Future Enhancements

* [ ] User accounts and favorites
* [ ] Recipe ratings and reviews
* [ ] Recipe scaling
* [ ] Export to PDF
* [ ] Mobile version
* [ ] More Telugu recipes

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

* Traditional Telugu cuisine
* Edamam Nutrition API
* OpenAI & LangChain
* Bootstrap & Flask communities

---

**Enjoy cooking authentic Telugu dishes! 🍛**
