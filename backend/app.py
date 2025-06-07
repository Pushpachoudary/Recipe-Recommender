from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes, allowing your React frontend to communicate with this Flask backend
CORS(app)

# Retrieve Spoonacular API key from environment variables for security
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
def index():
    # Simple endpoint to confirm the API is running
    return jsonify({"message": "Recipe Recommender API is running"})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get JSON data from the request body
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        diet = data.get('diet', '')
        time = data.get('time', None)  # time will be None if not provided or parsed to null by frontend

        # Validate if ingredients are provided
        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        # Construct comma-separated query string for ingredients
        query = ",".join(ingredients)
        url = "https://api.spoonacular.com/recipes/complexSearch"

        # Initialize parameters with mandatory fields
        params = {
            "apiKey": SPOONACULAR_API_KEY,
            "includeIngredients": query,
            "number": 5,
            "addRecipeInformation": True
        }

        # Optional filters
        if diet:
            params["diet"] = diet
        if time is not None:
            params["maxReadyTime"] = time

        # API call to Spoonacular
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error from Spoonacular API: {response.text}")
            return jsonify({"error": "Failed to fetch data from Spoonacular API", "details": response.text}), 500

        spoonacular_data = response.json()

        recipes = []
        for item in spoonacular_data.get('results', []):
            instructions = item.get("analyzedInstructions")
            steps = []
            if instructions and isinstance(instructions, list) and len(instructions) > 0:
                first_instruction_set = instructions[0]
                if 'steps' in first_instruction_set and isinstance(first_instruction_set['steps'], list):
                    steps = [step['step'] for step in first_instruction_set['steps'] if 'step' in step]

            recipes.append({
                "name": item.get("title"),
                "ingredients": [ing['name'] for ing in item.get("extendedIngredients", []) if 'name' in ing],
                "diet": diet or "Not specified",
                "time": item.get("readyInMinutes"),
                "calories": "N/A",  # Placeholder
                "steps": steps
            })

        # ✅ Return recipes wrapped in a key for safe parsing on frontend
        return jsonify({"recipes": recipes})

    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(debug=True)
