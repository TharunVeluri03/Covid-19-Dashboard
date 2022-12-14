import logging
from covid_data_handler import parse_csv_data, process_covid_csv_data, covid_API_request, schedule_covid_updates

logging.basicConfig(
    filename='logger.log',
    filemode='w',
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

def test_parse_csv_data ():
    data = parse_csv_data ('nation_2021-10-28.csv')
    assert len(data) == 639
    logging.info("test_parse_csv_data successfull")


def test_process_covid_csv_data ():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021 -10 -28. csv '))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544
    logging.info("test_process_covid_csv_data successfull")


def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, list)
    logging.info("test_covid_API_request successfull")

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=60, update_name="Test update for covid updates")
    logging.info("test_schedule_covid_updates successfull")
