# Telugu Recipes - Traditional Cuisine with Nutrition Data

A comprehensive web application for managing and discovering authentic Telugu recipes with nutrition information, structured data, and a powerful query interface.

## ✨ Features

### ✅ What You Have Now
- **Traditional Telugu Recipes**: Authentic Pulihora recipes and more
- **AI-Powered Diet Menu Generator**: LLM that creates personalized Telugu diet plans
- **Nutrition Data**: Automatic nutrition calculation based on ingredients
- **Structured Format**: Organized recipe database with ingredients, instructions, and metadata
- **Query Interface**: Beautiful web interface with search functionality
- **Modern UI**: Responsive design with beautiful gradients and animations

### 🔧 Technical Features
- **SQLite Database**: Efficient storage and retrieval of recipes
- **Nutrition API Integration**: Real-time nutrition calculation (with fallback to mock data)
- **Flask Web Framework**: Fast and reliable web application
- **Bootstrap 5**: Modern, responsive UI components
- **RESTful API**: JSON endpoints for programmatic access

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

5. **Initialize the database**
   Click the "Initialize" button in the navigation to add sample recipes

## 📁 Project Structure

```
telugu-llm/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database operations
├── nutrition_api.py       # Nutrition API integration
├── recipe_processor.py    # Recipe processing utilities
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── recipe_detail.html # Recipe detail page
│   ├── add_recipe.html   # Add recipe form
│   └── search_results.html # Search results page
└── README.md            # This file
```

## 🍽️ Sample Recipes Included

The system comes with 20+ authentic Telugu recipes across multiple categories:

### Breakfast (అల్పాహారం)
1. **Idli Sambar** - Steamed rice cakes with lentil soup
2. **Dosa Chutney** - Crispy rice crepes with coconut chutney
3. **Pongal** - Rice and lentil porridge
4. **Upma** - Semolina breakfast dish
5. **Puri Aloo Curry** - Deep-fried bread with potato curry
6. **Pesarattu** - Green moong dal crepes

### Main Course (ముఖ్య భోజనం)
7. **Classic Tamarind Pulihora** - Traditional sour rice dish
8. **Lemon Pulihora** - Tangy lemon-flavored rice
9. **Coconut Pulihora** - Rich coconut-infused rice
10. **Peanut Pulihora** - Nutty and flavorful rice dish
11. **Biryani** - Fragrant rice with meat and spices
12. **Ragi Mudde** - Finger millet balls

### Side Dishes (పక్క వంటకాలు)
13. **Gongura Pachadi** - Sorrel leaves chutney
14. **Gutti Vankaya** - Stuffed brinjal curry

### Snacks (చిరుతిండి)
15. **Mirchi Bajji** - Stuffed chili fritters
16. **Bonda** - Urad dal fritters

### Desserts (మిఠాయి)
17. **Pootharekulu** - Paper-thin sweet rolls
18. **Gavvalu** - Shell-shaped sweets

Each recipe includes:
- Complete ingredient list
- Step-by-step instructions
- Cooking time and difficulty level
- Calculated nutrition information

## 🤖 AI Diet Menu Generator (ఆహార పట్టిక జనరేటర్)

The system features an intelligent LLM that generates personalized diet menus in Telugu:

- **Natural Language Input**: Describe your diet needs in English or Telugu
- **Personalized Plans**: AI creates custom meal plans based on preferences
- **Health Goal Support**: Weight loss, diabetic, protein-rich, energy boost
- **Telugu Recommendations**: Comprehensive health advice in Telugu language
- **Nutrition Tracking**: Automatic calorie and nutrient calculation
- **Multi-day Plans**: Generate weekly or monthly diet plans
- **Category-based Selection**: Smart meal selection based on categories (breakfast, main course, etc.)

### Example Inputs:
- "vegetarian diet for weight loss, 1500 calories"
- "diabetic diet low sugar for a week"
- "protein rich diet for muscle gain"
- "బరువు తగ్గించడానికి శాకాహార ఆహారం"
- "మధుమేహం కోసం తక్కువ చక్కెర ఆహారం"
- "ప్రోటీన్ ఎక్కువగా ఉన్న ఆహారం"
- "శక్తి పెంపుకు శుద్ధ శాకాహారం"

## 🔍 Advanced Search & Customization

- **Advanced Search**: Filter by category, difficulty, cooking time, and tags
- **Search by recipe name**: Find specific dishes
- **Search by ingredients**: Discover recipes using available ingredients
- **Real-time results**: Instant search results
- **Nutrition filtering**: View recipes with nutrition data
- **Tag-based filtering**: Filter by vegetarian, protein-rich, healthy, quick, etc.
- **Category browsing**: Browse recipes by breakfast, main course, snacks, desserts
- **Customizable preferences**: Set dietary restrictions and health goals

## 📊 Nutrition Information

The system automatically calculates nutrition data for each recipe including:
- Calories per serving
- Protein content
- Carbohydrates
- Fat content
- Fiber
- Sugar
- Sodium

## 🛠️ API Endpoints

### GET `/api/recipes`
Returns all recipes in JSON format

### GET `/api/search?q=<query>`
Search recipes by name or ingredients

### POST `/add_recipe`
Add a new recipe to the database

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Gradients**: Beautiful color schemes
- **Interactive Cards**: Hover effects and animations
- **Real-time Preview**: See recipe preview while adding
- **Nutrition Charts**: Visual nutrition information
- **Search Interface**: Easy recipe discovery

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for API keys:

```env
NUTRITION_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

### Nutrition API
The system uses the Edamam Nutrition API. To get real nutrition data:
1. Register at [Edamam](https://developer.edamam.com/)
2. Get your API key
3. Add it to the `.env` file

Without an API key, the system uses intelligent mock data based on common Telugu ingredients.

## 📈 Database Schema

### Recipes Table
- `id`: Primary key
- `name`: Recipe name
- `ingredients`: JSON array of ingredients
- `instructions`: Cooking instructions
- `cooking_time`: Time in minutes
- `difficulty`: Easy/Medium/Hard
- `cuisine_type`: Telugu (default)
- `created_at`: Timestamp

### Nutrition Table
- `id`: Primary key
- `recipe_id`: Foreign key to recipes
- `calories`: Calories per serving
- `protein`: Protein in grams
- `carbs`: Carbohydrates in grams
- `fat`: Fat in grams
- `fiber`: Fiber in grams
- `sugar`: Sugar in grams
- `sodium`: Sodium in mg

## 🚀 Future Enhancements

- [ ] Recipe categories and tags
- [ ] User accounts and favorites
- [ ] Recipe ratings and reviews
- [ ] Image upload for recipes
- [ ] Recipe sharing functionality
- [ ] Mobile app version
- [ ] More Telugu recipes
- [ ] Recipe scaling (serving size adjustment)
- [ ] Export recipes to PDF
- [ ] Recipe recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your recipes or improvements
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Traditional Telugu cuisine and recipes
- Edamam Nutrition API for nutrition data
- Bootstrap for the beautiful UI components
- Flask community for the excellent web framework

---

**Enjoy cooking authentic Telugu dishes! 🍛** #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 #   t e l u g u - l l m  
 