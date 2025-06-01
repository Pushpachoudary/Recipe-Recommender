import os
import json

def load_recipes():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "recipes.json")
    with open(file_path, "r") as file:
        return json.load(file)

def recommend_recipes(user_ingredients, top_k=3):
    recipes = load_recipes()
    scores = []

    for recipe in recipes:
        match_count = len(set(user_ingredients) & set(recipe["ingredients"]))
        scores.append((recipe["title"], match_count))

    scores.sort(key=lambda x: x[1], reverse=True)
    return [title for title, score in scores if score > 0][:top_k]
