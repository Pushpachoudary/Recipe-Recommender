from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load recipes
def load_recipes():
    file_path = os.path.join(os.path.dirname(__file__), "recipes.json")
    with open(file_path, "r") as file:
        return json.load(file)

# Recipe recommendation logic
def recommend_recipes(ingredients, diet=None, time=None):
    recipes = load_recipes()
    filtered = []

    for recipe in recipes:
        if diet and recipe.get("diet", "").lower() != diet.lower():
            continue
        if time and recipe.get("time", 9999) > time:
            continue
        if not all(item.lower() in map(str.lower, recipe.get("ingredients", [])) for item in ingredients):
            continue
        filtered.append(recipe)

    return filtered

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        ingredients = data.get("ingredients", [])
        diet = data.get("diet")
        time = data.get("time")

        results = recommend_recipes(ingredients, diet, time)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
