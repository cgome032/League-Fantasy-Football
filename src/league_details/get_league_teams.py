import json
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
    teams = league_details.get_teams()
    first_owner = teams[0].owners[0]
    print(f"Single owner: {json.dumps(first_owner, indent=4)}")
    for team in teams:
        print(f"Team: {team} ID: {team.team_id}")

if __name__ == "__main__":
    container = ConfigurationReaderContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    main(*sys.argv[1:])
