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
from langchain_core.utils.json import parse_json_markdown

from langchain_groq import ChatGroq

from langchain.tools import tool
import requests
import logging
import json
import sys
import random

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
    data_dir = 'data/fiches/series'
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
    file_path_actuel = os.path.join('data', 'actuel.json')    
    with open(file_path_actuel, 'w') as file:
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

    url = f"https://api.themoviedb.org/3/search/tv?query={title}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    return data["results"][0]["id"]

def get_tv_credits(id):
    url = f"https://api.themoviedb.org/3/tv/{id}/credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + API_KEY_TMDB,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_actor= []
    for i in range(len(data["cast"])):
        if data["cast"][i]["order"] < 5:
            data_actor.append((data["cast"][i]["name"], data["cast"][i]["character"]))
    return data_actor

# def get_tv_recommandation(name):
#     id_tv = get_tv_id(name)
#     url = f"https://api.themoviedb.org/3/tv/{id_tv}/recommendations?language=en-US&page=1"

#     headers = {
#         "accept": "application/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYWM4ZWExYTUzOWFhMGViYjY0MGU5OWQ4Zjg1NmRmNyIsInN1YiI6IjY2NDVjNDUxMzJhZmYxMDA5YjVjMTI2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2iaGeBzCSVKz7LcS0Cdi3dv4k5Ws8ykNh-amI0NVuwo"
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()

#     results = data["results"]
#     sample_size = min(len(results), 10)
#     random_results = random.sample(results, sample_size)

#     data_list = []
#     for result in random_results:
#         data_list.append(result["name"])
#     return data_list

# def get_tv_popular():
#     url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY_TMDB}"
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
    
#     results = data["results"]
#     sample_size = min(len(results), 10)
#     random_results = random.sample(results, sample_size)
    
#     data_list = []
#     for result in random_results:
#         data_list.append({
#             "name": result["name"],
#             "popularity": result["popularity"]
#         })
        
#     return data_list

# def get_genre_list():
#     url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY_TMDB}"
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     genre_dict = {genre["name"]: genre["id"] for genre in data["genres"]}
#     return genre_dict

# def get_tv_popular_list():
#     url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY_TMDB}"
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     return data["results"]

# def get_tv_recommendation_genre(genre_name):
#     genre_dict = get_genre_list()
#     if genre_name not in genre_dict:
#         return []
#     genre_id = genre_dict[genre_name]
#     rec = get_tv_popular_list()
#     data = []
#     for tv in rec:
#         if genre_id in tv["genre_ids"]:
#             data.append(tv["name"])
#     return data

# def get_tv_recommendation_genre_name(title_substring, genre_name):
#     identifiant = get_tv_id(title_substring)
#     print(identifiant)
#     if not identifiant:
#         return f"No TV series found with title containing '{title_substring}'"
    
#     url = f"https://api.themoviedb.org/3/tv/{identifiant}/similar?language=en-US&page=1"
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {API_KEY_TMDB}"
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
    
#     genre_dict = get_genre_list()
#     print(genre_dict)
#     if genre_name not in genre_dict:
#         return f"Genre '{genre_name}' not found"
    
#     genre_id = genre_dict[genre_name]
#     similar_shows = data['results']
    
#     filtered_shows = [show for show in similar_shows if genre_id in show['genre_ids']]    
#     if not filtered_shows:
#         return f"No similar shows found in the genre '{genre_name}'"
    
#     sample_size = min(len(filtered_shows), 5)
#     random_show = random.sample(filtered_shows, sample_size)
#     recommended_tv = [movie["name"] for movie in random_show]

#     return recommended_tv



@tool
def get_tv(title: Annotated[str, "Title of the Tv Show"]) -> dict:
    """
    Retrieves detailed information about a series using the TMDB API, based on a supplied title. The function retrieves the series' first and last release dates, synopsis, director, top 5 actors, and other metadata such as length of last episode, number of seasons, number of episodes and genre.
    Parameters :
    query (str): The series title for the query.

    Example:
    >>> get_tv("Stranger Things")
    "FINISHED"
    
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
    You are a film specialist and can only answer in this field. A detailed understanding of the history of the conversation is essential to maintain context in follow-up questions.

    Expected entry format:
    - History entries are formatted as follows: '- Human: “Question”' followed by '- Bot: “Answer”'.
    - The last query should be formatted as follows: 'Query: “Follow-up question”'.

    If the follow-up question refers to a series mentioned previously but not explicitly named in the last query (e.g. “its budget?”), deduce the series name from the last relevant dialog where it was mentioned.
    Answer the human in the most useful and accurate way possible in your specialty. You have access to the following tools:

    {tools}
    If you use get_tv, the return is a JSON with details of the series. You need to look up the information in the JSON to respond.
    Use a json blob to specify a tool by providing an action key (tool name) and an action input key (tool input).

      Valid “action” values: “Final Answer” or {tool_names}

    Provide only ONE action per $JSON_BLOB, as shown:

    ```
    {{
    “action”: $TOOL_NAME,
    “action_input”: {{“query”: “$INPUT”}}
    }}
    ```

    Follow this format:

    Question: input question to be answered
    Reflection: take previous and next steps into account
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: action result
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to say
    Action:
    ```
    {{
   “action”: “Final Answer”,
    “action_input”: “Final response to human”
    }}
    The "Final response to human" must be in string format, don't put the answer in a dictionary.
    Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation'''

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
llm =ChatGroq(
        api_key="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",
        model="llama3-8b-8192")
# llm = ChatOpenAI(
#     temperature=0,
#     model_name="gpt-4-1106-preview",
#     openai_api_base="http://localhost:8000/v1",
#     openai_api_key="Not needed for local server",
# )

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