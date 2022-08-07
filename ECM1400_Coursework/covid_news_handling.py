import requests
import sched
import time
import sys
import json
import logging

from newsapi import NewsApiClient
from typing import Dict, List
from datetime import datetime
from traceback import format_exception, format_stack
from types import FunctionType


covidNews_scheduler = sched.scheduler(time.time, time.sleep)


with open('config.json', 'r') as f:
    config = json.load(f)
    API_keys = config["api_key"]
    covid_terms_con = config["search_terms"]

logging.basicConfig(
    filename='logger.log',
    filemode='w',
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

def news_API_request(covid_terms=covid_terms_con):
    """
    Returns up to date news articles
  
    Parameters:
    -covid_terms (str): Articles that mention gthese terms will be used.

    Returns:
    -titles_list: dictionary of the titles from the articles
    -description_list : dictionary of the content from the articles
    """

    params = {
    'q': 'Covid Covid-19 coronavirus',
    'sortBy': 'top',
    'language': 'en',
    "pageSize": 1,
    "page": 100
    }

    headers = {
        'X-Api-Key': API_keys,  # KEY in header to hide it from url
        }

    url = 'https://newsapi.org/v2/everything'

    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    global titles_list
    global description_list


    titles_list = []
    description_list = []

    articles = data["articles"]

    for article in articles:
        titles = [arr["title"] for arr in articles]
        description = [arr["content"] for arr in articles]

        titles_list.append(titles)
        description_list.append(description)
        logging.info("Covid articles fetched successfully")
    return titles_list, description_list
        
news_API_request()

def filter_list():
    """
    puts the covid news articles into a dictionary where they are together

    Parameters:

    Returns:

    """
    
    global news_layout

    news_layout = [
        {
            "title": titles_list,
            "content": description_list
        },
    ]

    global news


filter_list()
global all_news_layout
all_news_layout = news_layout


def reason():
    """
    This function prints "Updating all data on this page"
  
    Parameters:

    Returns:
    
    print("Updating all news articles on this page.")
    """
reason()

def schedule_covidNews_updates(update_interval = str, update_name = str, priority=1):
    """
    This function schedules covid updates for covid news articles
  
    Parameters:
    -update_interval (str): The interval to update covid data
    -update_name (str) : The name to give the update

    Returns:
    """

    covidNews_update = covidNews_scheduler.enter(update_interval, 1, reason(), (update_name,))
    covidNews_scheduler.run(covidNews_update)
    logging.info("Covid update is scheduled")

