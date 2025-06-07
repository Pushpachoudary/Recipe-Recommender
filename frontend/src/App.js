import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [diet, setDiet] = useState('');
  const [time, setTime] = useState('');
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/recommend`, {
        ingredients: ingredients.split(',').map((item) => item.trim()),
        diet: diet,
        time: time ? parseInt(time) : null
      });

      const receivedRecipes = Array.isArray(res.data)
        ? res.data
        : Array.isArray(res.data.recipes)
        ? res.data.recipes
        : [];

      setRecipes(receivedRecipes);
    } catch (err) {
      console.error("Error fetching recipes:", err);
      setError('Something went wrong while fetching recipes. Please try again.');
      setRecipes([]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 to-blue-100 p-6">
      <div className="max-w-3xl mx-auto bg-white shadow-2xl rounded-xl p-8">
        <h1 className="text-4xl font-extrabold text-center text-green-800 mb-8">🥗 Recipe Recommender</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            placeholder="Enter ingredients (comma-separated)"
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          <input
            type="text"
            placeholder="Diet (optional: vegetarian, vegan, etc)"
            value={diet}
            onChange={(e) => setDiet(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          <input
            type="number"
            placeholder="Max cooking time in minutes (optional)"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-green-400"
          />
          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-xl shadow-lg transition"
          >
            🔍 Get Recipes
          </button>
        </form>

        {loading && <p className="text-center mt-6 text-green-600 font-semibold">Loading recipes...</p>}
        {error && <p className="text-red-600 text-center mt-6 font-semibold">{error}</p>}

        <div className="mt-10 space-y-6">
          {!loading && recipes.length === 0 && !error && (
            <p className="text-center text-gray-600">No recipes found. Try different ingredients!</p>
          )}
          {recipes.map((recipe, idx) => (
            <div key={idx} className="p-6 border border-green-200 rounded-2xl shadow-md bg-green-50">
              <h2 className="text-2xl font-bold text-green-700 mb-2">{recipe.name}</h2>
              <p><span className="font-semibold">🍴 Ingredients:</span> {recipe.ingredients.join(', ')}</p>
              <p><span className="font-semibold">🧘 Diet:</span> {recipe.diet}</p>
              <p><span className="font-semibold">⏱️ Time:</span> {recipe.time} min</p>
              <p><span className="font-semibold">🔥 Calories:</span> {recipe.calories}</p>
              <p><span className="font-semibold">👨‍🍳 Steps:</span> {recipe.steps && recipe.steps.length > 0 ? recipe.steps.join(' → ') : 'Not available'}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
