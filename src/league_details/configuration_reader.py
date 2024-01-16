from dependency_injector import containers, providers

from league_configuration_data import LeagueConfigurationData
from league_details import BorrachosLeagueDetails
from league_fetcher import ESPNLeagueFetcher


class ConfigurationReaderContainer(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["league_configuration.ini"])

    league_configuration_data = providers.Singleton(
        LeagueConfigurationData,
        config.league.league_id.as_int(),
        config.league.season_year.as_int(),
        config.league.first_prize.as_int(),
        config.league.second_prize.as_int(),
        config.league.third_prize.as_int(),
        config.league.best_record_prize.as_int(),
        config.league.most_points_prize.as_int(),
        config.league.weekly_highest_score_prize.as_int(),
        config.league.team_buy_in.as_int(),
    )

    espn_league_fetcher = providers.Singleton(
        ESPNLeagueFetcher,
        config.league.league_id.as_int(),
        config.league.season_year.as_int(),
    )

    league_details = providers.Singleton(
        BorrachosLeagueDetails, league_configuration_data, espn_league_fetcher
    )
