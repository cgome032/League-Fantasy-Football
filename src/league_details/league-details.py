from espn_api.football import League, Team
from typing import List, Tuple

class BorrachosLeagueDetails:
    def __init__(self) -> None:
        self.setup()

        # This all needs to be changed to be configuration based per year using configparser or something similar
        self.position_winnings = {
            1: 300,
            2: 200,
            3: 150
        }
        self.best_record_winnings = 110
        self.most_points_winnings = 110
        self.weekly_winnings = 10
    
    def setup(self) -> None:
        self.league_id = 1866114
        self.season = 2020
        self.espn_endpoint = "https://fantasy.espn.com/apis/v3/games/FFL/seasons/" + str(self.season) + "/segments/0/leagues/" + str(self.league_id)

    def create_league(self) -> League:
        return League(self.league_id, self.season)

    def get_top_scorer(self) -> str:
        league = self.create_league()
        return league.top_scorer().team_name

    def get_best_regular_season_record(self) -> str:
        teams = self.get_teams()
        for team in teams:
            if team.standing == 1:
                return team.team_name
    
    def get_top_teams_winnings(self) -> dict:
        all_teams = self.get_teams()
        top_teams = dict()
        for team in all_teams:
            if team.final_standing in self.position_winnings:
                top_teams[team.team_name] = self.position_winnings[team.final_standing]
        return top_teams

    def get_weekly_scorers(self) -> List[Tuple]:
        league = self.create_league()
        highest_weekly_scorers = list()
        for week_number in range(1, 14):
            weekly_scoreboard = league.scoreboard(week_number)
            highest_team = (0, weekly_scoreboard[0].home_team.team_name, weekly_scoreboard[0].home_score)
            for matchup in weekly_scoreboard:
                home_details = (week_number, matchup.home_team.team_name, matchup.home_score)
                away_details = (week_number, matchup.away_team.team_name, matchup.away_score)
                matchup_leader = max(home_details, away_details, key=lambda t: t[2])
                highest_team = max(matchup_leader, highest_team, key=lambda t: t[2])
            highest_weekly_scorers.append(highest_team)
        return highest_weekly_scorers

    def get_teams(self) -> List[Team]:
        league = self.create_league()
        return league.teams

    def initialize_teams_payments(self) -> dict:
        teams_payment = { team.team_name: -100 for team in self.get_teams() }
        return teams_payment

    def get_teams_winnings_amount(self):
        all_teams = self.initialize_teams_payments()

        """
        Grab the winners of the following categories
        1st
        2nd
        3rd
        Weekly winners
        Best record
        Most points
        """
        best_record_team = self.get_best_regular_season_record()
        most_points_team = self.get_top_scorer()
        weekly_winners = self.get_weekly_scorers()
        top_teams = {k:v for k,v in sorted(self.get_top_teams_winnings().items(), key=lambda item: item[1], reverse=True)}

        print("Top placing teams")
        for place, (team, winnings) in enumerate(top_teams.items(), start=1):
            print( "{} place team {} wins ${}".format(place, team, winnings))
            all_teams[team] += top_teams[team]

        print("Weekly winners - each team wins ${}".format(self.weekly_winnings))
        for week_number, team_name, team_score in weekly_winners:
            print("Week {} winner: {} with {} points".format(week_number, team_name, team_score))
            all_teams[team_name] += self.weekly_winnings

        all_teams[best_record_team] += self.best_record_winnings
        all_teams[most_points_team] += self.most_points_winnings
        
        print("Best record team wins ${}: {}".format(self.best_record_winnings, best_record_team))
        print("Most points team wins ${}: {}".format(self.most_points_winnings, most_points_team))

        return all_teams


if __name__ == "__main__":
    leagueDetails = BorrachosLeagueDetails()

    teamsWinnings = leagueDetails.get_teams_winnings_amount()
    print("Teams winnings")
    for team, payment in teamsWinnings.items():
        print("{}: {}".format(team, payment))
