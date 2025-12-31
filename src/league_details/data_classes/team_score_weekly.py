from dataclasses import dataclass


@dataclass(frozen=True)
class TeamScoreWeekly:
    """
    Data class to encapsulate a team's weekly score
    """

    team_id: int
    week_number: int
    weekly_team_score: float
