import os
from langchain import hub
from langchain.agents import create_structured_chat_agent
from langchain_community.agent_toolkits.load_tools import load_tools
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




def get_movie_playing():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 5:
        limit = len(data["results"])
    else:
        limit = 5   
    for i in range(limit):
        data_list.append(data["results"][i]["title"])
    return data_list


def get_movie_popular():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append({
                    "title": data["results"][i]["title"],
                    "popularity": data["results"][i]["popularity"]
                })    
    return data_list

def get_movie_top_rated():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append(data["results"][i]["title"])
    return data_list

def get_movie_upcoming():
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append(data["results"][i]["title"])
    return data_list


def get_people_popular():
    url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append({
            "name": data["results"][i]["name"],
            "popularity": data["results"][i]["popularity"]
        })    
    return data_list

def get_tv_airing():
    url = "https://api.themoviedb.org/3/tv/airing_today?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append( data["results"][i]["name"])    
    return data_list

def get_tv_popular():
    url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append({
            "name": data["results"][i]["name"],
            "popularity": data["results"][i]["popularity"]
        })     
    return data_list

def get_tv_top_rated():
    url = "https://api.themoviedb.org/3/tv/top_rated?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY_TMDB}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    if len(data["results"]) < 10:
        limit = len(data["results"])
    else:
        limit = 10   
    for i in range(limit):
        data_list.append({
            "name": data["results"][i]["name"],
            "popularity": data["results"][i]["popularity"]
        })     
    return data_list

