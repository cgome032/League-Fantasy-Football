from dataclasses import dataclass


@dataclass(frozen=True)
class LeagueConfigurationData:
    """Configuration data for league"""

    league_id: int
    season_year: int
    first_prize: int
    second_prize: int
    third_prize: int
    best_record_prize: int
    most_points_prize: int
    weekly_highest_score_prize: int
    team_buy_in: int
    robot_team_ids: list[int]
