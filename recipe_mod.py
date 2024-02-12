from typing import Any
from langchain.agents import create_json_agent, Tool
from langchain_community.agent_toolkits import JsonToolkit
from langchain.prompts import PromptTemplate
from langchain_community.tools.json.tool import JsonSpec
from langchain_openai import ChatOpenAI
from tools import refine_search_tool

template = """
You specialize in generating recipes tailored to users' ingredient lists. Your task is to process a JSON object named 'hits,' which contains a 
  collection of recipes. Return the recipes as a Python dictionary adhering to the user's specifications.

JSON data: {data}

Input Prompt: {recipe_mod_prompt}

When identifying recipes that meet the user's criteria, examine each recipe dictionary for relevant details. The user may request dishes with specific attributes like spicy, healthy, gluten-free, or vegan.

Your final answer needs to be a dictionary in the same structure as the JSON data provided. You need to provide recipes that align with the user's prompt.

"""
# Instead if it is necessary, add additional keywords to this url after "q="
# https://api.edamam.com/search?q=&app_id=661e92a2&app_key=6ac45378dedb6f84360dc381a54241a4&to=10 and make a request.
# With this new JSON data, present the most relevant recipes to the user as JSON.

prompt_template = PromptTemplate(
    input_variables=["data", "recipe_mod_prompt"], template=template
)

def recipe_mod(data:str, recipe_mod_prompt:str)->Any:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    json_spec = JsonSpec(dict_=data, max_value_length=4000)
    json_toolkit = JsonToolkit(spec=json_spec)
    # tool = [
    #     Tool(
    #         name="Make a refined request to Edamam's API",
    #         func=refine_search_tool,
    #         description="useful for when none of the recipes align with the user's prompt and you are not able to provide a definite answer",
    #     )
    # ]

    json_agent_executor = create_json_agent(
        llm=llm,
        toolkit=json_toolkit,
        verbose=True,
        handle_parsing_errors=True
    )
    inputs = {"input": {"data": data, "recipe_mod_prompt": recipe_mod_prompt}}
    # print("INPUTS~~~~~~~~~~~~~~~~~~~~~~~~", inputs)
    # print("TYPE~~~~~~~~~~~~~~~~~~~~~~~~~~", type(data["hits"][0]))
    # print("HITS~~~~~~~~~~~~~~~~~~~~~~~~~~", data["hits"][0])
    # json_agent_executor.run({"input": inputs})
    json_agent_executor.run("List all the attributes of each hit and list recipes that are lower in sugar")
    # json_agent_executor.run("List all the different recipe labels from the JSON object provided.")