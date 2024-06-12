import os
from langchain import hub
from langchain.agents import create_react_agent,load_tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOllama
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
from langchain_core.prompts import PromptTemplate

from langchain_groq import ChatGroq
from typing import Literal, Dict
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




#TV TOOL

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY_TMDB = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYWM4ZWExYTUzOWFhMGViYjY0MGU5OWQ4Zjg1NmRmNyIsInN1YiI6IjY2NDVjNDUxMzJhZmYxMDA5YjVjMTI2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2iaGeBzCSVKz7LcS0Cdi3dv4k5Ws8ykNh-amI0NVuwo"



# Définition de l'outil avec annotations

def save_full_json(details: dict, actors_series: dict, actors_tv: dict, tv_id: str):
    # Chemin du fichier où enregistrer le JSON complet
    data_dir = 'data/fiches/person'
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"{tv_id}_details.json")
    # Créer la structure de données combinée
    full_data = {
        'details': details,
        'actors_series': actors_series,
        'actors_tv': actors_tv
    }
    
    # Enregistrer le JSON complet dans un fichier
    with open(file_path, 'w') as file:
        json.dump(full_data, file, indent=4)
    file_path_actuel = os.path.join('data', 'actuel.json')    
    with open(file_path_actuel, 'w') as file:
        json.dump(full_data, file, indent=4)  

def get_person_details(id):
    url = f"https://api.themoviedb.org/3/person/{id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def get_person_id(title):
    url = f"https://api.themoviedb.org/3/search/person?query={title}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["results"][0]["id"]

def get_person_movie_credits(id):
    url = f"https://api.themoviedb.org/3/person/{id}/movie_credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + API_KEY_TMDB,
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_actor= []
    if len(data["cast"]) < 5:
        limit = len(data["cast"])
    else:
        limit = 5    
    for i in range(limit):
        if data["cast"][i]["order"] < 5:
            data_actor.append((data["cast"][i]["original_title"], data["cast"][i]["character"]))
    return data_actor

def get_person_tv_credits(id):
    url = f"https://api.themoviedb.org/3/person/{id}/tv_credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_actor= []
    if len(data["cast"]) < 5:
        limit = len(data["cast"])
    else:
        limit = 5   
    for i in range(limit):
        if data["cast"][i]["episode_count"] > 5:
            data_actor.append((data["cast"][i]["name"], data["cast"][i]["character"]))
    return data_actor

def recommend_similar_tv_shows(tv_show_ids):
    recommendations = []
    for tv_show_id in tv_show_ids:
        url = f"https://api.themoviedb.org/3/tv/{tv_show_id}/recommendations?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY_TMDB}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            recommendations.extend(data["results"])
        else:
            print(f"Failed to fetch recommendations for TV show ID {tv_show_id}")

    # Eliminer les doublons par ID de série
    unique_recommendations = {rec['id']: rec for rec in recommendations}.values()

    # Trier par popularité décroissante et prendre les 5 premiers
    sorted_recommendations = sorted(unique_recommendations, key=lambda x: x["popularity"], reverse=True)
    
    # Renvoyer seulement les titres des séries recommandées
    recommended_titles = [rec["name"] for rec in sorted_recommendations[:5]]
    return recommended_titles

def recommend_similar_movies(movie_ids):
    recommendations = []
    for movie_id in movie_ids:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY_TMDB}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            recommendations.extend(data["results"])
        else:
            print(f"Failed to fetch recommendations for movie ID {movie_id}")

    # Eliminer les doublons par ID de film
    unique_recommendations = {rec['id']: rec for rec in recommendations}.values()

    # Trier par popularité décroissante et prendre les 5 premiers
    sorted_recommendations = sorted(unique_recommendations, key=lambda x: x["popularity"], reverse=True)
    recommended_titles = [rec["title"] for rec in sorted_recommendations[:5]]

    return recommended_titles


@tool
def get_recommendations_based_on_person(person_name: Annotated[str, "Name of the person"]):
    """
    Fetches movie and series recommendations based on the provided name of person.

    INPUT : Name of the person from the query

    Returns:
    dict: A dictionary containing a list of movies and series matches the query. Select the films and series in this list to build your final answer
    
    
    
    """

    # Obtenir l'ID de la personne
    person_id = get_person_id(person_name)
    
    # Obtenir les crédits de films et de séries
    movie_credits = get_person_movie_credits(person_id)
    tv_credits = get_person_tv_credits(person_id)
    
    # Extraire les IDs des films et séries les plus populaires (limité à 5)
    movie_ids = [movie[0] for movie in movie_credits[:5]]
    tv_show_ids = [tv_show[0] for tv_show in tv_credits[:5]]
    
    # Obtenir des recommandations basées sur ces films et séries
    movie_recommendations = recommend_similar_movies(movie_ids)
    tv_show_recommendations = recommend_similar_tv_shows(tv_show_ids)
    
    return {
        "movies": movie_recommendations,
        "tv_shows": tv_show_recommendations
}


InfoRequired = Literal['biography', 'birthday', 'deathday', 'name', 'actors_series', 'actors_tv']

@tool
def get_person(params: str) -> dict:
    """
    Fetches detailed information about a person (actor/realisator) from the TMDB API based on provided parameters in a single string.

    Parameters:
    
    params (str): A single string containing the name of the perosn and the type of information required, separated by a comma.
    Returns:
    str: A string representation of the requested person detail or a list of actors with his roles if 'actors_series' or 'actors_movies' is chosen.

    Example:
    get_movie("Denzel Washington, biography")
    """
    params_list = params.split(", ")
    query = params_list[0].strip()
    info_required = params_list[1].strip()
    logger.info(f"get_person called with name: {query}")
    name_id = get_person_id(query)
    details = get_person_details(name_id)
    actors_movies = get_person_movie_credits(name_id)
    actors_series = get_person_tv_credits(name_id)
    save_full_json(details, actors_movies, actors_series, name_id)
    answer = ""   


        
    if info_required == "actors_movies":
        answer = "\n".join(f"- {query} playing {actor[1]} in {actor[0]}"  for actor in actors_movies)
    elif   info_required == "actors_series":    
        answer = "\n".join(f"- {query} playing {actor[1]} in {actor[0]}" for actor in actors_series)
    else:
        if info_required in details:
            answer = f"The {info_required} is {details[info_required]}"
        else:
            answer = "The requested information is not available." 

    return {"answer" : answer}

@tool
def get_search(query: str) -> dict:
    """
    Use this tool to retrieve information that is not covered by other tools.

    Parameters:
    query (str): The query from the user seeking information.

    Returns:
    dict: The answer to the query, with the key 'answer'.

    Description:
    This tool leverages DuckDuckGo's search capabilities to find and provide information on a wide range of topics. When a user's query cannot be addressed by the specialized tools available, use this tool to perform a web search and return relevant information. It is particularly useful for general knowledge questions, current events, or any other queries that fall outside the scope of existing tools.
    """
    search = DuckDuckGoSearchRun()
    final_search = search.run(query)

    return {"answer" : final_search}

# FIN MOVIE TOOL



def create_custom_prompt():
    system = '''
   You are a film specialist and can only answer in that field. A detailed understanding of the history of the conversation is essential to maintain context in follow-up questions.

    Expected entry format:
    - Entries in the history are formatted as follows: '- Human: “Question”' followed by '- Bot: “Answer”'.
    - The last query should be formatted as follows: “Query: ‘Follow-up question’”.

    If the follow-up question refers to a person previously mentioned but not explicitly named in the last query (e.g. “his birthday”), deduce the person's name from the last relevant dialog where he was mentioned.
    Answer the human in the most useful and accurate way possible in your specialty. You have access to the following tools:

    {tools}
    If you use get_person, the return is a JSON with the person's details. You'll need to look up the information in the JSON to respond.
    Use a json blob to specify a tool by providing an action key (tool name) and an action input key (tool input).

    Valid "action" values: "Final Answer" or {tool_names}

    Provide only ONE action per $JSON_BLOB, as shown:

    ```
    {{
    "action": $TOOL_NAME,
    "action_input": {{"query": "$INPUT"}}
    }}
    ```

    Follow this format:

    Question: input question to answer
    Thought: consider previous and subsequent steps
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: action result
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to respond
    Action:
    ```
    {{
    "action": "Final Answer",
    "action_input": "Final response to human"
    }}

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
      get_search,
      get_person,
      get_recommendations_based_on_person
  ]

  tools.extend(load_tools(['wikipedia']))

  return tools

tools = get_function_tools()
# prompt = PromptTemplate.from_template("You are a movie assistant specialist in actor/realisator and your role is to answer the question using your tools. You don't have the right to use your knowledge to answer. You only need to retrieve the result provided by your tool and translate it into a sentence for the user. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat ONLY once)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question.\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}")
prompt = PromptTemplate.from_template("Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format strictly and do not add personal comments or observations:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat ONLY ONCE times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question.\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}")


# Choose the LLM that will drive the agent
# llm =ChatGroq(
#         api_key="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",
#         model="llama3-8b-8192")
llm = ChatOllama(
    model="llama3",
    temperature=0,
)

# Construct the OpenAI Functions agent
agent_runnable = create_react_agent(llm, tools, prompt)

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