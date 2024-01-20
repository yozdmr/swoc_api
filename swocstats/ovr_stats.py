# Import
from swocstats.utilities import scrape, url_constructor, CURR_YEAR, RESULT_TYPE_REF
import json



class SWOCLeagueStats:
    def __init__(self, sport):
        self.sport = sport



    # Gets the list of teams and their ID
    def get_teams(self, year:int = CURR_YEAR):
        # Process and remove 'position' and 'record'
        teams = self.get_standings(year=year)
        for entry in teams:
            entry.pop('position', None)
            entry.pop('record', None)

        # Convert back to JSON
        return json.dumps(teams, indent=4)


    # Gets the standings for the season
    def get_standings(self, year:int = CURR_YEAR):
        url = url_constructor(page_type="ovr", page_sub_type=0,
                            sport=self.sport, year=year)
        soup = scrape(url)

        tbody = soup.find(id="statsContent").find('tbody')

        standings = []
        position = 1  # Variable that indicates position
        for row in tbody.find_all('tr')[2:]:
            columns = row.find_all('td')

            if len(columns) == 5:  # Check num columns is good
                team_name = columns[0].get_text(strip=True)  # Team name
                team_id = columns[0].find('a')['href'].replace("&", "=").split("=")[3]  # Team id
                
                # Get list of results, make dict with result_type_list
                record_conf = dict(zip(RESULT_TYPE_REF, columns[1].get_text(strip=True).split(" - ")))
                record_ovr = dict(zip(RESULT_TYPE_REF, columns[3].get_text(strip=True).split(" - ")))

                standings.append({
                    "team_name":team_name,
                    "team_id":team_id,
                    "position":position,
                    "record":[
                        {"conference":record_conf},
                        {"overall":record_ovr} 
                    ]
                })

                position += 1
        
        # Convert the list of dictionaries to JSON
        return json.dumps(standings, indent=4)



    # Gets the player performance statistics for the season
    def get_statistics_ovr(self, year:int = CURR_YEAR):
        url = url_constructor(page_type="ovr", page_sub_type=1,
                            sport=self.sport, year=year)
        soup = scrape(url)

        tbody_left = soup.find(class_="column-one").find('tbody')
        tbody_right = soup.find(class_="column-two").find('tbody')
        
        statistics = []
        self._get_statistics_helper(statistics, tbody_left)
        self._get_statistics_helper(statistics, tbody_right)

        # Convert the list of dictionaries to JSON
        return json.dumps(statistics, indent=4)

    # Helper function to apply to both left and right tables
    def _get_statistics_helper(self, statistics:list, tbody):
        for row in tbody.find_all('tr'):  # Skip the header row
            # Extract the columns (td elements)
            columns = row.find_all('td')

            # If not td, is th - therefore, add section with name
            if len(columns) == 0:
                label_col = row.find('th').get_text(strip=True).lower()
                statistics.append({label_col:[]})

            else:  # Make sure that each row has 2 columns (Player and Value)
                # Gets the last appended key in the dictionary allowing
                #   the addition of the players from that category
                key = next(iter(statistics[len(statistics)-1]))

                # Divide data in first column
                data = columns[0].get_text(strip=True).replace("(", ".").replace("),\r\n", ".").split(".")
                
                # Extract data
                position = data[0]
                pts = columns[1].get_text(strip=True)
                player_name = data[1]
                player_id = columns[0].find('a')['href'].split("=")[1]
                grade = data[2]
                team = data[3].strip()

                # Add to statistics
                statistics[len(statistics)-1][key].append({
                    "position":position,
                    key:pts, 
                    "player_name":player_name,
                    "player_id":player_id,
                    "grade":grade,
                    "team":team
                })



    # Gets the teams participating in the conference that year
    def get_teams(self, year:int = CURR_YEAR):
        url = url_constructor(page_type="ovr", page_sub_type=2,
                            sport=self.sport, year=year)
        soup = scrape(url)

        tbody = soup.find(id="statsContent").find('tbody')
        teams = []

        for row in tbody.find_all('tr'):
            team_name = row.get_text().split(" \n")[0].strip()
            team_id = row.find('a')['href'].replace("&", "=").split("=")[3]
            teams.append({
                "team_name":team_name,
                "team_id":team_id
            })

        # Convert the list of dictionaries to JSON
        return json.dumps(teams, indent=4)



    # Gets the schedule for the season
    # def get_schedule(self, year:int = CURR_YEAR):



    # Gets the season's awards
    # def get_awards(year:int = CURR_YEAR):



    # Gets the list of champions in the history of SWOC
    def get_champions(self):
        url = url_constructor(page_type="ovr", page_sub_type=5,
                            sport=self.sport)
        soup = scrape(url)

        tbody = soup.find(id="statsContent").find('tbody')

        champions = []
        for row in tbody.find_all('tr')[1:]:  # Skip the header row
            # Extract the columns (td elements)
            columns = row.find_all('td')

            if len(columns) == 2:  # Make sure that each row has 2 columns (Team and Year)
                year = columns[0].get_text(strip=True)
                team = columns[1].get_text(strip=True)
                champions.append({team: year})

        # Convert the list of dictionaries to JSON
        return json.dumps(champions, indent=4)
