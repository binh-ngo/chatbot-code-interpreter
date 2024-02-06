from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import (
    create_csv_agent,
    create_python_agent,
)
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

load_dotenv()


def main():
    print("Start...")

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    python_agent_executor = create_python_agent(
        llm=llm,
        tool=PythonREPLTool(),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,  # this handling parsing error
    )

    # python_agent_executor.run(
    #     "Generate and save in current working directory 15 QRcodes that point to www.binhngo.me"
    # )

    csv_agent_executor = create_csv_agent(
        llm=llm,
        path="episode_info.csv",
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )

    # csv_agent_executor.run("How many columns are there in file, episode_info.csv")
    # csv_agent_executor.run("Which writer wrote the most episodes? How many episodes did they write?")
    # csv_agent_executor.run(
    #     "Print the seasons in ascending order based on the number of episodes they have."
    # )

    grand_agent = initialize_agent(
        tools=[
            Tool(
                name="PythonAgent",
                func=python_agent_executor.run,
                description="""Useful when you need to transform natural language and write from it in python and execute the python code,
                                returning the results of the code execution, 
                                DO NOT SEND PYTHON CODE TO THIS TOOL""",
            ),
            Tool(
                name="CSVAgent",
                func=csv_agent_executor.run,
                description="""Useful when you need to answer questons about episode_info.csv file,
                                takes an input's entire question and returns the answer after running pandas calculations""",
            ),
        ],
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
    # grand_agent.run(
    # "Generate and save in current working directory 15 QRcodes that point to www.binhngo.me, you have the qrcode package installed already"
    # )

    # grand_agent.run("Print the seasons in ascending order based on the number of episodes they have")

    grand_agent.run(
        "I want you to add unique ingredient_id numbers to each of the ingredients in the chef-ingredients csv file."
    )


if __name__ == "__main__":
    main()
