from hashlib import new
import logging

from flask import Flask, render_template, request
from covid_data_handler import get_covid_data, covid_API_request, global_covid_data
from covid_news_handling import news_API_request, all_news_layout



# Create our flask app
app = Flask(__name__)

logging.basicConfig(
    filename='logger.log',
    filemode='w',
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

get_covid_data()


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    """
    This function displays the content that we want it to display
    :return: render the html page
    """
    logging.info("Flask for Covid Dashboard page started successfully")

    hospital_cases = global_covid_data['HospitalCases']
    national_deaths = global_covid_data['DeathsTotal']
    local_confirm = global_covid_data['local7DayCases']
    national_confirm = global_covid_data['national7DayCases']
    web_hospital_cases = "National hospital cases:", str(hospital_cases)
    deaths = "National death total: ", str(national_deaths)

# all_news_layout

    return render_template(
        "index.html",
        title="Coronavirus Dashboard",
        location="Exeter",
        nation_location="England",
        image="favicon.png",
        news_articles = all_news_layout,
        local_7day_infections= local_confirm,
        national_7day_infections = national_confirm,
        hospital_cases = web_hospital_cases,
        deaths_total = deaths,

    )

if __name__ == '__main__':
    app.run() 