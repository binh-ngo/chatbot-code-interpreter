from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.tools import PythonREPLTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
 
load_dotenv()
 
 
def main():
    print("Start...")

    # llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # python_agent_executor = create_python_agent(
    #     llm=llm,
    #     tool=PythonREPLTool(),
    #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True,
    #     handle_parsing_errors=True,  # this handling parsing error
    # )

    # python_agent_executor.run(
    #     "Generate and save in current working directory 15 QRcodes that point to www.binhngo.me"
    # )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    csv_agent_executor = create_csv_agent(
        llm=llm,
        path="episode_info.csv",
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
 
    # csv_agent_executor.run("How many columns are there in file, episode_info.csv")
    # csv_agent_executor.run("Which writer wrote the most episodes? How many episodes did they write?")
    csv_agent_executor.run(
        "Print the seasons in ascending order based on the number of episodes they have."
    )
 
 
if __name__ == "__main__":
    main() 
