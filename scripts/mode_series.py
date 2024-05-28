import os
from langchain import hub
from langchain.agents import create_structured_chat_agent,load_tools
from langchain_openai.chat_models import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.graph import END, StateGraph
from langsmith import trace
import operator

from langchain.tools import tool
import requests
import logging
import json
import sys


# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Multi-agent Collaboration"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"




#MOVIE TOOL

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY_TMDB = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYWM4ZWExYTUzOWFhMGViYjY0MGU5OWQ4Zjg1NmRmNyIsInN1YiI6IjY2NDVjNDUxMzJhZmYxMDA5YjVjMTI2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2iaGeBzCSVKz7LcS0Cdi3dv4k5Ws8ykNh-amI0NVuwo"



# Définition de l'outil avec annotations
# Définition de l'outil avec annotations

def save_full_json(details: dict, actors: dict, tv_id: str):
    # Chemin du fichier où enregistrer le JSON complet
    data_dir = 'data/series'
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"{tv_id}_details.json")
    # Créer la structure de données combinée
    full_data = {
        'details': details,
        'actors': actors
    }
    
    # Enregistrer le JSON complet dans un fichier
    with open(file_path, 'w') as file:
        json.dump(full_data, file, indent=4)


def get_tv_details(id):
    url = f"https://api.themoviedb.org/3/tv/{id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def get_tv_id(title):
    print(title)
    url = f"https://api.themoviedb.org/3/search/tv?query={title}&include_adult=false&language=en-US&page=1"
    print(url)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    return data["results"][0]["id"]

def get_tv_credits(id):
    url = f"https://api.themoviedb.org/3/tv/{id}/credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + API_KEY_TMDB,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print("dekfdkdkodkofkdof")
    print(data)
    data_actor= []
    for i in range(len(data["cast"])):
        if data["cast"][i]["order"] < 5:
            data_actor.append((data["cast"][i]["name"], data["cast"][i]["character"]))
    return data_actor

@tool
def get_tv(title: Annotated[str, "Title of the Tv Show"]) -> dict:
    """
    Fetches detailed information about a TV show from the TMDB API based on the title provided in the query.
    This function retrieves the TV show's detailed data sheet including its release date, synopsis, season details,
    and other relevant metadata. Additionally, it retrieves the list of the top actors involved in the TV show.
    
    Parameters:
    title (str): The title of the TV show for which details are being fetched. This title is used to query the TMDB API.
    
    Returns:
    dict: A dictionary containing 'details' and 'actors' keys, each holding comprehensive information about the TV show and its cast.
    
    Example:
    >>> get_tv("Stranger Things")
    {'details': {...}, 'actors': [...]}
    
    Detailed information retrieved includes:
    - Last air date
    - First air date
    - Number of seasons
    - Number of episodes
    - Information about Last episode : episode runtime, note, name of episode, overview
    - Release date
    - TV show synopsis
    - Season details
    - List of top actors
    - Other relevant metadata such as number of episodes, genres, and more.
    - Network
    - Created By
    
    Note:
    This function calls several helper functions:
    - get_tv_id() to retrieve the unique identifier for the TV show.
    - get_tv_details() to fetch the TV show's main data sheet.
    - get_tv_credits() to obtain the list of top actors involved in the show.
    - save_full_json() to save all the retrieved information in a JSON format.
    """
    logger.info(f"get_tv called with tv title: {title}")
    tv_id = get_tv_id(title)
    details = get_tv_details(tv_id)
    actors = get_tv_credits(tv_id)
    save_full_json(details, actors, tv_id)    
    return {"details": details, "actors": actors}



# FIN MOVIE TOOL



def create_custom_prompt():
    system = '''
    Respond to the human as helpfully and accurately as possible. You have access to the following tools:
    {tools}

    Use a JSON object to specify a tool by providing an "action" key (tool name) and an "action_input" key (tool input).
    The response from each tool will be in the form of a dictionary. Your task is to extract relevant information from this dictionary to answer the human's query with sentence.

    Valid "action" values: "Final Answer" or {tool_names}

    Provide only ONE action per JSON object, as shown:

    ```
    {{
    "action": "$TOOL_NAME",
    "action_input": {{"query": "$INPUT"}}
    }}
    ```

    Follow this format:

    Question: input question to answer
    Thought: consider previous and subsequent steps, ensure you understand how to extract information from the dictionary response of the tool
    Action:
    ```
    {{
    "action": "$TOOL_NAME",
    "action_input": {{"query": "$INPUT"}}
    }}
    ```
    Observation: Extract specific information from the dictionary to construct your response
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to respond
    Action:
    ```
    {{
    "action": "Final Answer",
    "action_input": "Final response to human"
    }}
    ```

    The final response in "action_input" must strictly be the output without any additional elements or modifications.

    Begin! Reminder to ALWAYS respond with a valid JSON object for each action. Use tools if necessary. Respond directly if appropriate. Format is Action:```json
    {{
    "action": "$TOOL_NAME",
    "action_input": {{"query": "$INPUT"}}
    }}
    ``` then Observation.

    IMPORTANT:
    '''

    human = '''{input}

    {agent_scratchpad}

    (reminder to respond in a JSON object no matter what)'''

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", human),
        ]
    )
    return prompt

def get_function_tools():
  search = TavilySearchAPIWrapper()
  tavily_tool = TavilySearchResults(api_wrapper=search)

  tools = [
      tavily_tool,
      get_tv,
  ]

  tools.extend(load_tools(['wikipedia']))

  return tools

tools = get_function_tools()
prompt = create_custom_prompt()

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4-1106-preview",
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="Not needed for local server",
)

# Construct the OpenAI Functions agent
agent_runnable = create_structured_chat_agent(llm, tools, prompt)

class AgentState(TypedDict):
    # The input string
    input: str
    # The list of previous messages in the conversation
    chat_history: list[BaseMessage]
    # The outcome of a given call to the agent
    # Needs `None` as a valid type, since this is what this will start as
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # List of actions and corresponding observations
    # Here we annotate this with `operator.add` to indicate that operations to
    # this state should be ADDED to the existing values (not overwrite it)
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


tool_executor = ToolExecutor(tools)


# Define the agent
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}


# Define the function to execute tools
def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}


# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
    else:
        return "continue"

# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()    

def process_movie(input_data):
    inputs = {"input": input_data, "chat_history": []}
    results = []
    i = 0
    for s in app.stream(inputs):
        results.append(list(s.values())[0])
        i += 1
    retour = results[i-1]["agent_outcome"].return_values.get("output", "")
    return f"{retour}"

if __name__ == "__main__":
    input_data = sys.argv[1]
    result = process_movie(input_data)
    print(json.dumps({"result": result}))