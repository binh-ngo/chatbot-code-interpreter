import streamlit as st
import pandas as pd
import requests
import os
import math
from dotenv import load_dotenv

load_dotenv()

app_key = os.environ.get("EDAMAM_APPLICATION_KEY")
app_id = os.environ.get("EDAMAM_APPLICATION_ID")

# Read the CSV file
df = pd.read_csv("updated-file.csv")
# Extract unique ingredients
ingredients_list = df["ingredient"].unique()

# if "recipe_history" not in st.session_state:
#     st.session_state["user_prompt_history"] = []

# Streamlit app
st.header("Sous Chef Chatbot")
selected_ingredients = st.multiselect(
    options=ingredients_list, label="Ingredients you want to use"
)

if st.button("Find Recipes"):
    # Construct the query string for selected ingredients
    query = ",".join(selected_ingredients)

    params = {
       "q": query,
       "app_id": app_id,
       "app_key": app_key,
       "to": 3
    }

    # Replace 'YOUR_APP_ID' and 'YOUR_APP_KEY' with your actual Edamam application ID and key
    url = f"https://api.edamam.com/search"

    # Make the fetch request to the Edamam Recipe API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe_data = response.json()
        hits = recipe_data.get("hits", [])
        for hit in hits:
          recipe = hit.get("recipe", {})
          st.write(recipe.get("label", "No Label Available"))
          st.image(recipe.get("image", "No Image Available"))
          st.write("Yield:", recipe.get("yield", "N/A"))
          st.write("Calories per serving:", math.trunc(recipe.get("calories", "N/A")/recipe.get("yield", "N/A")))
          st.write("Total Time:", recipe.get("totalTime", "N/A"))
          st.write("Ingredients:")
          for ingredient in recipe.get("ingredientLines", []):
              st.write("- ", ingredient)
          st.write("----------")
    else:
      st.error("Failed to fetch recipe data. Please try again.")

# Store selected ingredients in session state
# st.session_state["user_prompt_history"].append(selected_ingredients)

