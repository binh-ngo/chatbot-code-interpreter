import pandas as pd

# Read the CSV file
df = pd.read_csv("updated-file.csv")

# # Define the mapping of specific words to substitutes
# word_to_substitute = {
#     'butter': ['margarine', 'ghee', 'oil'],
#     'fish sauce': ['salt', 'soy sauce', 'tamari', 'braggs liquid aminos', 'coconut aminos'],
#     'vinegar': ['lemon juice', 'lime juice', 'tamarind paste']
#     # Add more ingredient substitutions as needed
# }

# # Create a function to assign substitutes based on specific words
# def assign_substitute(ingredient):
#     for word, substitutes in word_to_substitute.items():
#         if word.lower() in ingredient.lower():
#             return substitutes if isinstance(substitutes, list) else [substitutes]
#     return ['No substitute']  # If no specific word matches, indicate no substitute

# # Apply the function to create a new 'substitute_for' column
# df['substitute_for'] = df['ingredient'].apply(assign_substitute)

# def replace_category(df):
#     """
#     Replace the 'vegetables' category with 'produce' in a DataFrame.

#     Parameters:
#     df (DataFrame): Input DataFrame containing the 'category' column.

#     Returns:
#     DataFrame: DataFrame with the 'vegetables' category replaced by 'produce'.
#     """
#     # Replace 'vegetables' with 'produce' in the 'category' column
#     df['category'] = df['category'].replace('vegetables', 'produce')
#     return df

# df = replace_category(df)

# Save the filtered DataFrame to a new CSV file
df.to_csv("updated-file.csv", index=False)
