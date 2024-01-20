from swocstats import SWOCLeagueStats, SWOCTeamStats

stats = SWOCLeagueStats(7)

sample = stats.get_teams(2018)

print(sample)