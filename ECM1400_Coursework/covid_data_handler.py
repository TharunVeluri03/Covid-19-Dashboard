import sys
import csv
import json
import sched
import time
import logging

from typing import Dict, List, Any
from uk_covid19 import Cov19API
from datetime import datetime, timedelta
from traceback import format_exception, format_stack
from types import FunctionType
from os import path, getcwd

covid_scheduler = sched.scheduler(time.time, time.sleep)


logging.basicConfig(
    filename='logger.log',
    filemode='w',
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

with open('config.json', 'r') as f:
    config = json.load(f)
    location_con = config["location"]
    locationType_con = config["location_type"]
    national_location_con = config["nation_location"]

def parse_csv_data(csv_filename):
    """
    This function returns data from a csv file. 
  
    Parameters:
    csv_filename : This is the filename
  
    Returns:
    A list of strings containing covid data.
  
    """

    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csv_data = []
        for row in reader:
            csv_data.append(row)
    
    logging.info("csv data was fetched successfully from a csv file")

    return csv_data


def read_cell(x, y):
    with open('nationwork.csv', 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1


def process_covid_csv_data(covid_csv_data):

    """
    Returns the number of cases in the last 7 days, current number of hospital
    cases and the cumulative number of deaths based on the given data 

    Parameters:
    covid_csv_data : A list of strings containing covid data.
  
    Returns:
    - last7days_cases : The last 7 days from the csv file
    - current_hospital_cases : The total number of hospital cases from the csv file
    - total_deaths : The total deaths from the csv file
    """
    
    # last7days_cases
    column = 3
    row = 6
    last7days_cases = 0
    i = 0
    while i < 7:
        last7days_cases = last7days_cases + int(read_cell(row, column))
        column = column + 1
        i = i + 1
    # current_hospital_cases
    current_hospital_cases = int(read_cell(5, 1))
    # total_deaths
    total_deaths = int(read_cell(4, 14))

    logging.info("The number of cases in the last 7 days was fetched successfully")
    logging.info("The number of hospital cases fetched successfully")
    logging.info("The total number of deaths fetched successfully")
    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location= location_con, location_type= locationType_con) -> str:

    """
    This function returns data from a csv file. 
  
    Parameters:
    location : Exeter : The location which data is taken from in the API
    location_type : ltla
  
    Returns:
    All covid data fetched from API

    """

    filters = [
        "areaType="+(location_type),
        "areaName="+(location)
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

    api = Cov19API(filters=filters, structure=cases_and_deaths)

    data = api.get_json()
    logging.info("Covid data fetched successfully from an API")

    return data


def get_covid_data():
    """
    This function uses the data from data and gets the local 7 day cases, national 7 day cases, total deaths and total hospital cases
  
    Parameters:

    Returns:
    
    """
    global covid_data

    england_only = [
        'areaType=nation',
        'areaName=England'
    ]

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    national_data = api.get_json()

    filters = [
        'areaType=ltla',
        'areaName=Exeter'
    ]
    api = Cov19API(filters=filters, structure=cases_and_deaths)
    data = api.get_json()
    global covid_data

    covid_data = {
        'local7DayCases' : 0,
        'HospitalCases' : 0,
        'DeathsTotal' : 0,
        'national7DayCases' : 0,
    }

    actual_data = data['data']
    nation_data = national_data['data']

    for key in range(0,8):
        if actual_data[key]['newCasesBySpecimenDate']:
            covid_data['local7DayCases'] += actual_data[key]['newCasesBySpecimenDate']
            logging.info("Local 7 Day Cases fetched successfully")

    covid_data['DeathsTotal'] = actual_data[1]['cumDeaths28DaysByPublishDate']
    covid_data['HospitalCases'] = actual_data[1]['hospitalCases']

    for key in range(0,8):
        if nation_data[key]['newCasesBySpecimenDate']:
            covid_data['national7DayCases'] += nation_data[key]['newCasesBySpecimenDate']
            logging.info("National 7 Day Cases fetched successfully")
    
    logging.info("The local number of cases in the last 7 days was fetched successfully from API")
    logging.info("The national number of cases in the last 7 days was fetched successfully from API")
    logging.info("The total nationa deaths was fetched successfully")
    logging.info("The total national hospital cases was fetched successfully")

get_covid_data()
global global_covid_data
global_covid_data = covid_data

def reason():
    """
    This function prints "Updating all data on this page"
  
    Parameters:

    Returns:
    
    """
    print("Updating all data on this page.")
reason()

def hhmm_to_seconds( hhmm: str ) -> int:


   return int(str(hhmm).split(':')[0])*60*60+int(str(hhmm).split(':')[1])*60

def schedule_covid_updates(update_interval = str, update_name = str, priority=1):
    """
    This function schedules covid updates
  
    Parameters:
    -update_interval (str): The interval to update covid data

    Returns:
    """

    covid_update = covid_scheduler.enter(update_interval, 1, reason(), (update_name,))
    covid_scheduler.run(covid_update)
    logging.info("Covid update is scheduled")

