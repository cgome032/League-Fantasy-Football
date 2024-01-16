import sys

from dependency_injector.wiring import inject, Provide

from configuration_reader import ConfigurationReaderContainer
from league_details import BorrachosLeagueDetails
from team_name_converter import get_team_owner


@inject
def main(
    league_details: BorrachosLeagueDetails = Provide[
        ConfigurationReaderContainer.league_details
    ],
) -> None:
    teams_winnings = league_details.get_teams_winnings_amount()
    for team_id, payment in teams_winnings.items():
        print("{}: {}".format(get_team_owner(team_id), payment))


if __name__ == "__main__":
    container = ConfigurationReaderContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    main(*sys.argv[1:])
