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
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "includeIngredients": query,
            "diet": diet,
            "maxReadyTime": time if time else None,
            "number": 5,
            "addRecipeInformation": True
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from Spoonacular API", "details": response.text}), 500

        data = response.json()

        recipes = []
        for item in data.get('results', []):
            instructions = item.get("analyzedInstructions")
            steps = [step['step'] for step in instructions[0]['steps']] if instructions and len(instructions) > 0 and 'steps' in instructions[0] else []

            recipes.append({
                "name": item.get("title"),
                "ingredients": [ing['name'] for ing in item.get("extendedIngredients", [])],
                "diet": diet or "Not specified",
                "time": item.get("readyInMinutes"),
                "calories": "N/A",  # Add nutrition API if needed
                "steps": steps
            })

        return jsonify(recipes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(debug=True)
