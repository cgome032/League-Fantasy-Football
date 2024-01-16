from abc import abstractmethod, ABC

from espn_api.football import League


class LeagueFetcher(ABC):
    """Fetch details about league"""

    def __init__(self, league_id: int, year: int) -> None:
        self.league_id = league_id
        self.year = year

    @abstractmethod
    def fetch_league(self) -> League:
        pass


class ESPNLeagueFetcher(LeagueFetcher):
    def fetch_league(self) -> League:
        return League(self.league_id, self.year)
