# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json
# import os

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all domains on all routes

# # Load recipes from a local JSON file
# with open('recipes.json', 'r', encoding='utf-8') as file:
#     recipes = json.load(file)

# # Optional: Load Spoonacular API key from environment variable
# # SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

# def recommend_recipes(ingredients, top_n=5):
#     """
#     Simple recommender: returns recipes with the most overlapping ingredients.
#     """
#     recommended = []
#     for recipe in recipes:
#         recipe_ingredients = set(map(str.lower, recipe.get('ingredients', [])))
#         input_ingredients = set(map(str.lower, ingredients))
#         match_count = len(recipe_ingredients & input_ingredients)
#         if match_count > 0:
#             recommended.append((match_count, recipe))

#     # Sort recipes by match count in descending order
#     recommended.sort(reverse=True, key=lambda x: x[0])
#     return [r[1] for r in recommended[:top_n]]

# @app.route('/')
# def index():
#     return jsonify({"message": "Recipe Recommender API is running"})

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     try:
#         data = request.get_json()
#         ingredients = data.get('ingredients', [])
#         if not ingredients:
#             return jsonify({"error": "No ingredients provided"}), 400

#         recommendations = recommend_recipes(ingredients)
#         return jsonify({"recipes": recommendations})  # ✅ Match frontend expectation
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
def index():
    return jsonify({"message": "Recipe Recommender API is running"})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        diet = data.get('diet', '')
        time = data.get('time', '')

        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        # Construct query
        query = ",".join(ingredients)
        url = f"https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "includeIngredients": query,
            "diet": diet,
            "maxReadyTime": time if time else None,
            "number": 5,
            "addRecipeInformation": True
        }

        response = requests.get(url, params=params)
        data = response.json()

        recipes = []
        for item in data.get('results', []):
            recipes.append({
                "name": item.get("title"),
                "ingredients": [ing['name'] for ing in item.get("extendedIngredients", [])],
                "diet": diet or "Not specified",
                "time": item.get("readyInMinutes"),
                "calories": "N/A",  # Can be added with extra API call
                "steps": [step['step'] for step in item.get("analyzedInstructions", [{}])[0].get("steps", [])]
            })

        return jsonify(recipes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
