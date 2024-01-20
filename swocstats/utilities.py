# Imports
import requests
from bs4 import BeautifulSoup
import datetime


# Gets the current year to analyze the latest data
def get_curr_year():
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    if current_month >= 8:  # August or later
        return current_year
    else:
        return current_year - 1

# Links beautifulsoup4 to the webpage
def scrape(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        return BeautifulSoup(response.text, 'html.parser')

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def url_constructor(sport:int = 7, year:int = 2023, team:int = 72, player:int = 679633, 
                    page_type:str = "ovr", page_sub_type:int = 5):
    # Swoc Sports URL
    url_base = "http://swocsports.com/"

    # Different possible pages
    pages_list = [
        ["confStandings", "scStatistics", "scTeams", "scAwards", "confSchedule", "scChampions"],
        ["scTeamStats", "scTeamSchedule", "scTeamRoster"],
        ["scPlayerStats"]
    ]

    # Which index of pages_list to go to
    page_dict = {
        "ovr": 0,
        "team": 1,
        "player": 2
    }

    page = pages_list[
        page_dict[page_type]
    ][page_sub_type]

    # Set base url
    url = url_base + f"{page}.aspx?"
    if page_type != "player":  # If not player
        url = url + f"sat={sport}&cmp=1&year={year}"  # Add necessary info
        if page_type == "team":  # If team, add team ID
            url = url + f"&schoolid={team}"
    else:  # If player, add player ID
        url = url + f"player={player}"

    return url



# Variables
CURR_YEAR = get_curr_year()

MONTH_REF = {
    "july": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11
}

RESULT_TYPE_REF = ["W", "L", "D"]