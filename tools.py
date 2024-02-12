import os
import requests
from typing import Any
from dotenv import load_dotenv
load_dotenv()

app_key = os.environ.get("EDAMAM_APPLICATION_KEY")
app_id = os.environ.get("EDAMAM_APPLICATION_ID")


def refine_search_tool(keywords:str)->Any:
  """Extracts additional keywords from user prompt and refines search"""
  params = {"q": keywords, "app_id": app_id, "app_key": app_key}
  url = f"https://api.edamam.com/search"
  response = requests.get(url, params=params)
  
  return response

