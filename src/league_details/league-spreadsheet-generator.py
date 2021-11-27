from espn_api.football import League
import csv
from datetime import date

class DataFetcher:
    """
    Fetch data from espn football api. 
    """
    def __init__(self, league_id, season_year) -> None:
        self.league = League(league_id, season_year)

    def get_teams(self):
        return self.league.teams

class DataFormatter:
    def __init__(self, data_fetcher: DataFetcher) -> None:
        if data_fetcher is None:
            raise TypeError("DataFetcher is None")
        
        self.data_fetcher = data_fetcher
        self._league_data = []
        self._format_team_info()
    
    def _format_team_info(self):
        for team in self.data_fetcher.get_teams():
            team_information = []
            team_information.append(team.team_name)
            team_information.append(team.points_for)
            team_information.append(team.points_against)
            team_information.append(team.wins)
            team_information.append(team.losses)
            team_information.append(team.ties)
            team_information.append(team.playoff_pct)
            team_information.extend(team.scores)
            self._league_data.append(team_information)
    
    def get_team_data(self):
        print(self._league_data)
        return self._league_data

class DataCSVOutputter:
    def __init__(self, data: list) -> None:
        if not isinstance(data, list):
            raise TypeError("Data needs to be in a list object.")

        self.output_data = data
        week_list_headers = ["Week {}".format(day) for day in range(1,15)]
        self._headers_list = [
            "Team name",
            "Points for",
            "Points against",
            "Wins",
            "Losses",
            "Ties",
            "Playoff PCT"
            ]
        self._headers_list.extend(week_list_headers)

    def create_csv_file(self):
        """
        Write the csv file of the data
        """
        todays_date = date.today()
        filename_string = "{}-league-information-spreadsheet.csv".format(todays_date)
        with open(filename_string, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self._headers_list)
            for team_info in self.output_data:
                writer.writerow(team_info)


if __name__ == "__main__":
    league_id = 1866114
    league_year = 2021
    data_fetcher = DataFetcher(league_id=league_id, season_year=league_year)
    data_formatter = DataFormatter(data_fetcher=data_fetcher)
    csv_outputter = DataCSVOutputter(data_formatter.get_team_data())
    csv_outputter.create_csv_file()