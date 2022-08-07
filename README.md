# Covid19-Dashboard
Automatic covid dashboard for displaying accurate, up to date covid data and news.

## Table of Contents

 - [Features](#features)
 - [Config File](#config_file)
 - [How To Use Application](#How_To_Use_Application)
 - [Disclaimer](#Disclaimer)
 - [Author](#author)


## Features
 This Dashboard contains upto date covid statistics and news articles with the ablitiy to schedule updates and more.

## Config File

This project has a configuration JSON file which can be used to customize the dashboard.

The default configuration is as follows:

```json
{
    "api_key": "your api key",
    "location": "Exeter",
    "location_type": "ltla",
    "nation_location": "England",
    "search_terms": "Covid COVID-19 coronavirus",
    "favicon": "favicon.png"

}
```

For the code to work please chage the required parameters to fit your need.

### Running Tests

Running the tests is a simple task.  
Firstly ensure the `pytest` module is installed.  

    pip install pytest

After this, ensure you are in the root directory before running

    pytest

If this doesn't work try running `python -m pytest`

## How To Use Application
When the website loads you will see three different sections.

In the centre of the dashboard you will see the local 7 day cases, national 7 day cases, hospital cases and total deaths( currently displays no values)

On the left hand side of the dashboard you will see the scheduled updates. When an update is scheduled then a title and and its description should be given.

On the right hand side you will see a list of news articles that when removed will not appear again.

## Author
Tharun Veluri
