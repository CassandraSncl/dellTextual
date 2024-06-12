import os
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.agent_toolkits.load_tools import load_tools
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
from langchain_core.prompts import PromptTemplate
from langsmith import trace
import operator
from langchain_core.utils.json import parse_json_markdown
import random

from typing import Literal, Dict

from langchain_groq import ChatGroq

from langchain.tools import tool
import requests
import logging
import json
import sys


# Set environment variables
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
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

def save_full_json(details: dict, actors: dict, movie_id: str):
    # Chemin du fichier où enregistrer le JSON complet
    data_dir = 'data/fiches/movies'
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"{movie_id}_details.json")


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

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    details = response.json()
    logger.info(f"get_movie_details returning details: {details}")
    return details

def get_movie_id(title):
    logger.info(f"get_movie_id called with title: {title}")
    url = f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    movie_id = data["results"][0]["id"]
    logger.info(f"get_movie_id returning movie_id: {movie_id}")
    return movie_id

def get_movie_credits(id):
    url = f"https://api.themoviedb.org/3/movie/"+str(id)+"/credits?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_actor= []
    for i in range(len(data["cast"])):
        if data["cast"][i]["order"] < 5:
            data_actor.append((data["cast"][i]["name"], data["cast"][i]["character"]))
    return data_actor



def get_movie_recommandation(title):
    movie_id = get_movie_id(title)
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    results = data["results"]
    sample_size = min(len(results), 10)
    random_results = random.sample(results, sample_size)

    data_list = []
    for result in random_results:
        data_list.append(result["title"])
    return data_list


def get_movie_popular() -> dict:

    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    results = data["results"]
    sample_size = min(len(results), 10)
    random_results = random.sample(results, sample_size)

    data_list = []
    for result in random_results:
        data_list.append({
            "title": result["title"],
            "popularity": result["popularity"],
        })

    return data_list

def get_movie_popular_list():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["results"]


def get_genre_list():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    genre_dict = {genre["name"]: genre["id"] for genre in data["genres"]}
    return genre_dict

def get_movie_recommendation_genre(genre_name):
    genre_dict = get_genre_list()
    if genre_name not in genre_dict:
        return []
    genre_id = genre_dict[genre_name]
    rec = get_movie_popular_list()
    data = []
    for movie in rec:
        if genre_id in movie["genre_ids"]:
            data.append(movie["title"])
    return data


def get_movie_recommendation_genre_name(title_substring, genre_name):
    identifiant = get_movie_id(title_substring)
    if not identifiant:
        return []

    url = f"https://api.themoviedb.org/3/movie/{identifiant}/similar?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    genre_dict = get_genre_list()
    if genre_name not in genre_dict:
        return []

    genre_id = genre_dict[genre_name]
    similar_movies = data["results"]
    
    filtered_movies = [movie for movie in similar_movies if genre_id in movie["genre_ids"]]

    if not filtered_movies:
        return []

    # Prendre 5 films aléatoires parmi ceux qui correspondent au genre
    sample_size = min(len(filtered_movies), 5)
    random_movies = random.sample(filtered_movies, sample_size)

    recommended_movies = [movie["title"] for movie in random_movies]
    
    return recommended_movies


InfoRequired = Literal['budget', 'genres', 'overview', 'popularity', 'production_companies', 'release_date', 'revenue', 'runtime', 'title', 'vote_average', 'vote_count', 'actors']
@tool
def get_movie(params: str) -> dict:
    """
    Fetches detailed information about a movie from the TMDB API based on provided parameters in a single string.

    Parameters:
    
    params (str): A single string containing the title of the movie and the type of information required, separated by a comma.
                The type of information must be one of the following:
                  budget, genres, overview, popularity, production_companies, release_date, revenue, runtime, title, vote_average, vote_count, actors

    Returns:
    str: A string representation of the requested movie detail or a list of actors with their roles if 'actors' is chosen.

    Example:
    get_movie("Inception, overview")
    """# Split the parameters
    params_list = params.split(", ")
    query = params_list[0].strip()
    info_required = params_list[1].strip()

    logger.info(f"get_movie called with movie title: {query} and information required: {info_required}")
    movie_id = get_movie_id(query)
    details = get_movie_details(movie_id)
    actors = get_movie_credits(movie_id)
    save_full_json(details, actors, movie_id)
    answer = ""

    if info_required == "actors":
        answer = "\n".join(f" {actor[0]} playing {actor[1]}" for actor in actors)
        answer = "The main actors are : " + answer
    else:
        if info_required in details:
            answer = f"The {info_required} is {details[info_required]}"
        else:
            answer = "The requested information is not available."

    return {"answer" : answer}


@tool
def get_recommendation(params: str) -> dict:
    """
    Fetches movie recommendations based on the provided title and/or genre.
    Input should be :
        - If title and genre : format : title, genre
        - If title : format : title, None
        - If genre : format : None, genre
        - If neither : format : None, None   
    Genre Available : Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History,Horror,Music,Mystery,Romance,Science Fiction,TV Movie,Thriller,War,Western

    Returns:
    dict: A dictionary containing a list of movies matches the query. Select the films in this list to build your final answer
    
    """
    
    parts = params.split(',')

    # Initialiser les variables
    title = None
    genre = None

    # Parcourir les parties séparées et extraire les valeurs
# Parcourir les parties séparées et extraire les valeurs
    if len(parts) >= 2:
        title_part = parts[0].strip()
        genre_part = parts[1].strip().split(' ')[0]  # Prendre uniquement "None" pour le genre

        # Assigner les valeurs
        title = title_part if title_part.lower() != "none" else None
        genre = genre_part if genre_part.lower() != "none" else None
    recommendations = []
    
    if title and genre:
        logger.info(f"title: {title} genre : {genre}")
        # Fetch recommendations based on both title and genre
        answer =f"The recommandations for {title} and genre {genre} are :"
        recommendations = get_movie_recommendation_genre_name(title, genre)

    elif title:
        logger.info(f"title: {title} genre : {genre}")
        # Fetch recommendations based on title
        answer =f"The recommandations for {title} are :"
        recommendations = get_movie_recommandation(title)

    elif genre:
        logger.info(f"title: {title} genre : {genre}")
        # Fetch recommendations based on genre
        answer =f"The recommandations for genre {genre} are :"
        recommendations = get_movie_recommendation_genre(genre)
    else:
        logger.info(f"Nothing")
        # Fetch general recommendations
        answer =f"The recommandations are :"
        recommendations = get_movie_popular()

    result = "\n".join(f"- {film}" for film in recommendations) 
    answer += result


    return {"answer": recommendations}







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

def get_function_tools():
  tools = [
      get_search,
      get_recommendation,
      get_movie
  ]


  return tools


def create_custom_prompt():
    system = '''
   You are a film specialist and can only answer in that field. A detailed understanding of the history of the conversation is essential to maintain context in follow-up questions.

    Expected entry format:
    - Entries in the history are formatted as follows: '- Human: “Question”' followed by '- Bot: “Answer”'.
    - The last query should be formatted as follows: “Query: ‘Follow-up question’”.

    If the follow-up question refers to a person previously mentioned but not explicitly named in the last query (e.g. “his birthday”), deduce the person's name from the last relevant dialog where he was mentioned.
    Answer the human in the most useful and accurate way possible in your specialty. You have access to the following tools:

    {tools}

    You can use get_recommandation only once. With the output, do an answer

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




tools = get_function_tools()
# prompt = PromptTemplate.from_template("You are a movie assistant and your role is to answer the question using your tools. You don't have the right to use your knowledge to answer. You only need to retrieve the result provided by your tool and translate it into a sentence for the user. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat ONLY once)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question.\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}")
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
    inputs = data.copy()
    if len(inputs["intermediate_steps"]) > 5:
        inputs["intermediate_steps"] = inputs["intermediate_steps"][-5:]
    agent_outcome = agent_runnable.invoke(inputs)
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