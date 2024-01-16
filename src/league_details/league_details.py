import sys

from dependency_injector.wiring import Provide, inject
from espn_api.football import League, Team
from typing import List, Tuple

from league_configuration_data import LeagueConfigurationData
from league_fetcher import LeagueFetcher


class BorrachosLeagueDetails:
    """
    League Details
    """

    def __init__(
        self, league_data: LeagueConfigurationData, league_fetcher: LeagueFetcher
    ) -> None:
        # This all needs to be changed to be configuration based per year using configparser or something similar
        self.position_winnings = {
            1: league_data.first_prize,
            2: league_data.second_prize,
            3: league_data.third_prize,
        }
        self.best_record_winnings = league_data.best_record_prize
        self.most_points_winnings = league_data.most_points_prize
        self.weekly_winnings = league_data.weekly_highest_score_prize
        self.season = league_data.season_year
        self.league_id = league_data.league_id
        self.team_buyin = league_data.team_buy_in
        self.espn_endpoint = (
            "https://fantasy.espn.com/apis/v3/games/FFL/seasons/"
            + str(self.season)
            + "/segments/0/leagues/"
            + str(self.league_id)
        )
        self.league_details = league_fetcher.fetch_league()

    def get_top_scorer(self) -> Team:
        """
        :return: Top scorer Team
        """
        return self.league_details.top_scorer()

    def get_best_regular_season_record(self) -> Team:
        teams = self.get_teams()
        for team in teams:
            if team.standing == 1:
                return team

    def get_top_teams_winnings(self) -> dict:
        all_teams = self.get_teams()
        top_teams = dict()
        for team in all_teams:
            if team.final_standing in self.position_winnings:
                top_teams[team.team_id] = self.position_winnings[team.final_standing]
        return top_teams

    def get_weekly_scorers(self) -> List[Tuple]:
        highest_weekly_scorers = list()
        for week_number in range(1, 14):
            weekly_scoreboard = self.league_details.scoreboard(week_number)
            highest_team = (
                0,
                weekly_scoreboard[0].home_team.team_id,
                weekly_scoreboard[0].home_score,
            )
            for matchup in weekly_scoreboard:
                home_details = (
                    week_number,
                    matchup.home_team.team_id,
                    matchup.home_score,
                )
                away_details = (
                    week_number,
                    matchup.away_team.team_id,
                    matchup.away_score,
                )
                matchup_leader = max(home_details, away_details, key=lambda t: t[2])
                highest_team = max(matchup_leader, highest_team, key=lambda t: t[2])
            highest_weekly_scorers.append(highest_team)
        return highest_weekly_scorers

    def get_teams(self) -> List[Team]:
        return self.league_details.teams

    def initialize_teams_payments(self) -> dict:
        """
        Initialize team by team ID
        :return:
        """
        teams_payment = {team.team_id: -self.team_buyin for team in self.get_teams()}
        return teams_payment

    def get_teams_winnings_amount(self) -> dict:
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
        top_teams = {
            k: v
            for k, v in sorted(
                self.get_top_teams_winnings().items(),
                key=lambda item: item[1],
                reverse=True,
            )
        }

        print("Top placing teams")
        print(f"Top teams: {top_teams.items()}")
        for place, (team, winnings) in enumerate(top_teams.items(), start=1):
            print("{} place team {} wins ${}".format(place, team, winnings))
            print(f"all_teams: {all_teams.items()}")
            all_teams[team] += top_teams[team]

        print("Weekly winners - each team wins ${}".format(self.weekly_winnings))
        for week_number, team_id, team_score in weekly_winners:
            print(
                "Week {} winner: {} with {} points".format(
                    week_number, team_id, team_score
                )
            )
            all_teams[team_id] += self.weekly_winnings

        all_teams[best_record_team.team_id] += self.best_record_winnings
        all_teams[most_points_team.team_id] += self.most_points_winnings

        print(
            "Best record team wins ${}: {}".format(
                self.best_record_winnings, best_record_team
            )
        )
        print(
            "Most points team wins ${}: {}".format(
                self.most_points_winnings, most_points_team
            )
        )

        return all_teams
