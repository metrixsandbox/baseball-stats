from unittest.mock import patch

from src.database.models import Player, Game, SeasonStats, TeamStats
from src.services.game_update_service import GameUpdateService


class TestGameUpdateService:
    def _make_service(self, session):
        """Create a GameUpdateService wired to the test session."""
        with patch("src.services.game_update_service.get_session", return_value=session):
            svc = GameUpdateService()
        return svc

    def test_adds_game_record(self, session):
        svc = self._make_service(session)
        game_data = {
            "date": "2025-04-17",
            "home_team": "ATL",
            "away_team": "PHI",
            "home_score": 7,
            "away_score": 3,
        }
        result = svc.update_after_game(game_data)
        assert result is True
        assert session.query(Game).count() == 1
        game = session.query(Game).first()
        assert game.home_team == "ATL"
        assert game.home_team_score == 7

    def test_updates_team_wins_losses(self, session):
        session.add(TeamStats(
            team_name="Atlanta Braves", year=2025, wins=90, losses=70,
            team_batting_avg=0.267, team_home_runs=245,
            team_runs_scored=800, team_runs_allowed=650,
            division_rank=1, team_era=3.45, team_strikeouts=1524,
            team_saves=42, team_whip=1.18,
        ))
        session.commit()

        svc = self._make_service(session)
        game_data = {
            "date": "2025-04-17",
            "home_team": "ATL",
            "away_team": "PHI",
            "home_score": 7,
            "away_score": 3,
        }
        svc.update_after_game(game_data)

        stats = session.query(TeamStats).filter_by(team_name="Atlanta Braves").first()
        assert stats.wins == 91
        assert stats.losses == 70
        assert stats.team_runs_scored == 807
        assert stats.team_runs_allowed == 653

    def test_updates_player_stats(self, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as session:
            player = Player(name="Ronald Acuña Jr.", team="ATL", position="RF",
                            batting_average=0.325, home_runs=42, runs_batted_in=98)
            session.add(player)
            session.flush()
            player_id = player.id

            session.add(SeasonStats(
                player_id=player_id, year=2025, games_played=155,
                batting_average=0.325, home_runs=42, runs_batted_in=98,
            ))
            session.commit()

        with Session(engine) as session:
            svc = self._make_service(session)
            game_data = {
                "date": "2025-04-17",
                "home_team": "ATL",
                "away_team": "PHI",
                "home_score": 7,
                "away_score": 3,
                "player_stats": [{
                    "name": "Ronald Acuña Jr.",
                    "at_bats": 4,
                    "hits": 2,
                    "home_runs": 1,
                    "rbi": 3,
                }],
            }
            svc.update_after_game(game_data)

        with Session(engine) as session:
            ss = session.query(SeasonStats).filter_by(player_id=player_id).first()
            assert ss.games_played == 156
            assert ss.home_runs == 43
            assert ss.runs_batted_in == 101

    def test_creates_new_season_stats_for_unknown_player_season(self, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as session:
            player = Player(name="New Guy", team="ATL", position="LF",
                            batting_average=0.0, home_runs=0, runs_batted_in=0)
            session.add(player)
            session.flush()
            player_id = player.id
            session.commit()

        with Session(engine) as session:
            svc = self._make_service(session)
            game_data = {
                "date": "2025-04-17",
                "home_team": "ATL",
                "away_team": "PHI",
                "home_score": 5,
                "away_score": 2,
                "player_stats": [{
                    "name": "New Guy",
                    "at_bats": 3,
                    "hits": 1,
                    "home_runs": 0,
                    "rbi": 1,
                }],
            }
            svc.update_after_game(game_data)

        with Session(engine) as session:
            ss = session.query(SeasonStats).filter_by(player_id=player_id).first()
            assert ss is not None
            assert ss.games_played == 1
            assert ss.runs_batted_in == 1

    def test_rollback_on_error(self, session):
        svc = self._make_service(session)
        # Missing required keys should trigger an error and rollback
        result = svc.update_after_game({})
        assert result is False
