import streamlit as st
import pandas as pd
import requests
import os
import math
from dotenv import load_dotenv
from recipe_mod import recipe_mod
load_dotenv()

app_key = os.environ.get("EDAMAM_APPLICATION_KEY")
app_id = os.environ.get("EDAMAM_APPLICATION_ID")

# Read the CSV file
df = pd.read_csv("updated-file.csv")
# Extract unique ingredients
ingredients_list = df["ingredient"].unique()

if "recipe_history" not in st.session_state:
    st.session_state["recipe_history"] = []

# Streamlit app
st.header("Sous Chef Chatbot")
selected_ingredients = st.multiselect(
    options=ingredients_list,
    label="Ingredients you want to use",
    placeholder="Choose ingredients",
)
# Construct the query string for selected ingredients
query = ",".join(selected_ingredients)

params = {"q": query, "app_id": app_id, "app_key": app_key}

# Replace 'YOUR_APP_ID' and 'YOUR_APP_KEY' with your actual Edamam application ID and key
url = f"https://api.edamam.com/search"


# print(recipe_mod_prompt==True)

recipe_mod_prompt = st.text_input(
    "Recipe Modifications", placeholder="Enter modifications here..."
)

if st.button("Find Recipes"):

  # Make the fetch request to the Edamam Recipe API
  response = requests.get(url, params=params)
# print(url, params)
# remove items with FREE in the health labels
  if response.status_code == 200:
      recipe_data = response.json()
      # print("RECIPE DATA:", recipe_data)
      new_json = {"q": query, "hits": []}

  for hit in recipe_data["hits"]:
      recipe = hit["recipe"]
      health_labels = [label for label in recipe["healthLabels"] if "Free" not in label]
      diet_labels = [label for label in recipe["dietLabels"] if "Free" not in label]

      new_hit = {
          "label": recipe["label"],
          "image": recipe["image"],
          "url": recipe["url"],
          "yield": recipe["yield"],
          "calories": recipe["calories"],
          "totalTime": recipe["totalTime"],
          "cuisineType": recipe["cuisineType"],
          "dietLabels": diet_labels,
          "healthLabels": health_labels,
          "ingredientLines": recipe["ingredientLines"],
      }
      new_json["hits"].append(new_hit)
      # print(new_json)

  # print("NEW JSON:", new_json)

  # print(new_json)
  if recipe_mod_prompt:
      # removes limit of recipes retrieved
      params["to"] = None
      new_response = requests.get(url, params=params)
      if response.status_code == 200:
          new_recipe_data = new_response.json()
          # print("NEW RECIPE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", new_recipe_data)
          all_new_json = {"q": query, "hits": []}

          for hit in new_recipe_data["hits"]:
              recipe = hit["recipe"]
              health_labels = [
                  label for label in recipe["healthLabels"] if "Free" not in label
              ]
              diet_labels = [
                  label for label in recipe["dietLabels"] if "Free" not in label
              ]

              new_hit = {
                  "label": recipe["label"],
                  "cuisineType": recipe["cuisineType"],
                  "dietLabels": diet_labels,
                  "healthLabels": health_labels,
                  # "ingredientLines": recipe["ingredientLines"],
              }
              all_new_json["hits"].append(new_hit)
          print(all_new_json)
              # print("ALLNEWJSON~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", all_new_json)

          recipe_mod(all_new_json, recipe_mod_prompt)

  for hit in new_json["hits"]:
      st.write(hit.get("label", "No Label Available"), " - ", hit.get("url", "N/A"))
      st.write(
          "Total Time:",
          recipe.get("totalTime", "N/A"),
          "mins | ",
          " Yield:",
          hit.get("yield", "N/A"),
          "| Calories per serving:",
          math.trunc(hit.get("calories", "N/A") / hit.get("yield", "N/A")),
      )
      st.image(hit.get("image", "No Image Available"))
      col1, col2 = st.columns(2)
      with col1:
        st.write("Health Labels:")
        for label in health_labels:
          st.write("- " + label)  
      with col2:
        st.write("Diet Labels:")
        for label in diet_labels:
          st.write("- " + label)  
      st.write("Ingredients:")
      for ingredient in recipe.get("ingredientLines", []):
          st.write("- ", ingredient)
      st.write("----------")
      st.session_state["recipe_history"].append(new_json)
  # else:
  #     st.error("Failed to fetch recipe data. Please try again.")
