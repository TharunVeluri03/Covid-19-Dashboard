import logging
from covid_news_handling import news_API_request, schedule_covidNews_updates

logging.basicConfig(
    filename='logger.log',
    filemode='w',
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

def test_news_API_request():
    news_API_request()
    assert news_API_request("Covid COVID-19 coronavirus") == news_API_request()
    logging.info("test_news_API_request successfull")

def test_schedule_covidNews_updates():
    schedule_covidNews_updates(update_interval=60, update_name="Test update for covid articles")
    logging.info("test_schedule_covidNews_updates successfull")