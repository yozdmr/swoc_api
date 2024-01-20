from swocstats.utilities import scrape, url_constructor, CURR_YEAR, MONTH_REF, RESULT_TYPE_REF
import json



class SWOCTeamStats:
    def __init__(self, sport):
        self.sport = sport



# Gets the stats of a team
def get_team_stats(self, team:int, year:int = CURR_YEAR):
    url = url_constructor(page_type="team", page_sub_type=0, team=team,
                          sport=self.sport, year=year)
    soup = scrape(url)

    tables = soup.find(id="statsContent").find_all('table')
    stats = []

    # Get offensive stats
    offensive_table = tables[0]
    title = offensive_table.find('th').get_text(strip=True).replace(" ", "-").lower()
    stats.append({title:[]})

    tbody = offensive_table.find('tbody')
    for row in tbody.find_all('tr')[1:]:
        columns = row.find_all('td')

        player_id = columns[0].find('a')
        if player_id != None:
            player_id = player_id['href'].split("=")[1]
            player_name = columns[0].get_text(strip=True).split("(")[0]
            games_played = columns[1].get_text(strip=True)
            goals = columns[2].get_text(strip=True)
            assists = columns[3].get_text(strip=True)
            points = columns[4].get_text(strip=True)
        
            stats[0][title].append({
                "player_name":player_name,
                "player_id":player_id,
                "games_played":games_played,
                "goals":goals,
                "assists":assists,
                "points":points
            })
    

    # Get defensive stats
    defensive_table = tables[1]
    title = defensive_table.find('th').get_text(strip=True).replace(" ", "-").lower()
    stats.append({title:[]})

    tbody = defensive_table.find('tbody')
    for row in tbody.find_all('tr')[1:]:
        columns = row.find_all('td')

        player_id = columns[0].find('a')
        if player_id != None:
            player_id = player_id['href'].split("=")[1]
            player_name = columns[0].get_text(strip=True).split("(")[0]
            games_played = columns[1].get_text(strip=True)
            goals_allowed = columns[2].get_text(strip=True)
            saves = columns[3].get_text(strip=True)
            save_perc = columns[4].get_text(strip=True)
            shutouts = columns[5].get_text(strip=True)
        
            stats[1][title].append({
                "player_name":player_name,
                "player_id":player_id,
                "games_played":games_played,
                "goals_allowed":goals,
                "saves":assists,
                "save_perc":points,
                "shutouts":shutouts
            })

    # Convert the list of dictionaries to JSON
    return json.dumps(stats, indent=4)



# Gets the roster of a team
def get_team_roster(self, team:int, year:int = CURR_YEAR):
    url = url_constructor(page_type="team", page_sub_type=2, team=team,
                          sport=self.sport, year=year)
    soup = scrape(url)

    tbody = soup.find(id="statsContent").find('tbody')

    roster = []
    for row in tbody.find_all('tr')[1:]:
        columns = row.find_all('td')

        number = columns[0].get_text(strip=True)
        player_name = columns[1].get_text(strip=True)
        player_id = columns[1].find('a')['href'].split("=")[1]
        grade = columns[2].get_text(strip=True)
        positions = columns[3].get_text(strip=True).split(",")

        roster.append({
            "player_name":player_name,
            "player_id":player_id,
            "squad_number":number,
            "grade":grade,
            "positions":positions
        })
    
    return json.dumps(roster, indent=4)



# Gets the schedule for the specified team
def get_team_schedule(self, team:int, year:int = CURR_YEAR):
    url = url_constructor(page_type="team", page_sub_type=1, team=team,
                          sport=self.sport, year=year)
    soup = scrape(url)

    tbody = soup.find(id="statsContent").find('tbody')

    schedule = []
    for row in tbody.find_all('tr'):
        columns = row.find_all('td')

        # If column type is header
        if len(columns) == 0:
            label_col = row.find('th').get_text(strip=True).lower().split(". ")[0]
            schedule.append({label_col:[]})
        
        else:
            # Gets the last appended key in the dictionary allowing
            #   the addition of the games in that month to that dict
            key = next(iter(schedule[len(schedule)-1]))

            # Handle the date
            date_raw = columns[0].get_text(strip=True).split('. ')
            date_month, date_day, day = label_col.split('. ')[0], date_raw[1], date_raw[0]
            date = f"{MONTH_REF[date_month]}/{date_day}/{year}"


            # Handle opponent info
            opponent = columns[1].get_text(strip=True).split(" ")
            home = True
            league_game = False
            if len(opponent) == 2:
                opponent = opponent[1]
                home = False
            else:
                opponent = opponent[0]

            opponent_id = -1
            if columns[1].find('a') != None:
                opponent_id = columns[1].find('a')['href'].split("=")[3]
                league_game = True
            

            # Handle score
            result_raw = columns[2].get_text(strip=True).split(' ')
            result = result_raw[0]
            result = "D" if result == "T" else result  # Change T for Tie to D for Draw because T is stupid
            result_score = result_raw[1]

            cup_game = False
            if "Postseason" in result_score:
                result_score = result_score.replace("Postseason", "")
                cup_game = True

            # Handle records
            records_raw = columns[3].get_text(strip=True)[:-1].split(" (")
            record_ovr = dict(zip(RESULT_TYPE_REF, records_raw[0].split("-")))
            record_conf = dict(zip(RESULT_TYPE_REF, records_raw[1].split("-")))


            schedule[len(schedule)-1][key].append({
                "date":date,
                "day":day,
                "opponent_name":opponent,
                "opponent_id":opponent_id,
                "home_game":home,
                "league_game":league_game,
                "cup_game":cup_game,
                "result":result,
                "result_score":result_score,
                "record":[
                    {"record_conf":record_conf},
                    {"record_ovr":record_ovr}
                ],
            })

    
    return json.dumps(schedule, indent=4)
