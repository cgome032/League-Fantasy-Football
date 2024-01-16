from abc import ABC, abstractmethod


class LeagueDetailsFormatter(ABC):
    @abstractmethod
    def handle_data(self, data: dict):
        pass


class LeagueDetailsFormatterSTDOut(LeagueDetailsFormatter):
    def handle_data(self, data: dict):
        """
        Grab the winners of the following categories
        1st
        2nd
        3rd
        Weekly winners
        Best record
        Most points
        """
        print("Top placing teams")
        for place, (team, winnings) in enumerate(top_teams.items(), start=1):
            print("{} place team {} wins ${}".format(place, team, winnings))

        print("Weekly winners - each team wins ${}".format(self.weekly_winnings))
        for week_number, team_name, team_score in weekly_winners:
            print(
                "Week {} winner: {} with {} points".format(
                    week_number, team_name, team_score
                )
            )

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
