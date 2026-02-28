from src.database.models import Player, Game, SeasonStats, TeamStats
from src.database.db_manager import add_record, get_all_records, update_record


class TestPlayerModel:
    def test_add_player(self, session):
        player = Player(
            name="Test Player",
            team="TST",
            position="CF",
            batting_average=0.300,
            home_runs=10,
            runs_batted_in=50,
        )
        session.add(player)
        session.commit()

        result = session.query(Player).filter_by(name="Test Player").first()
        assert result is not None
        assert result.name == "Test Player"
        assert result.team == "TST"
        assert result.batting_average == 0.300
        assert result.home_runs == 10

    def test_player_required_fields(self, session):
        """Players must have name, team, and position."""
        player = Player(name="A", team="B", position="C")
        session.add(player)
        session.commit()
        assert player.id is not None
        assert player.batting_average is None
        assert player.home_runs is None


class TestGameModel:
    def test_add_game(self, session):
        game = Game(
            date="2025-04-16",
            home_team="ATL",
            away_team="NYM",
            home_team_score=6,
            away_team_score=2,
        )
        session.add(game)
        session.commit()

        result = session.query(Game).first()
        assert result.home_team == "ATL"
        assert result.away_team == "NYM"
        assert result.home_team_score == 6

    def test_multiple_games(self, session):
        games = [
            Game(date="2025-04-16", home_team="ATL", away_team="NYM",
                 home_team_score=6, away_team_score=2),
            Game(date="2025-04-17", home_team="NYM", away_team="ATL",
                 home_team_score=3, away_team_score=8),
        ]
        session.add_all(games)
        session.commit()
        assert session.query(Game).count() == 2


class TestSeasonStatsModel:
    def test_season_stats_linked_to_player(self, session):
        player = Player(name="Test", team="TST", position="1B")
        session.add(player)
        session.flush()

        stats = SeasonStats(
            player_id=player.id,
            year=2025,
            games_played=100,
            batting_average=0.280,
            home_runs=20,
            runs_batted_in=60,
        )
        session.add(stats)
        session.commit()

        result = session.query(SeasonStats).filter_by(player_id=player.id).first()
        assert result.year == 2025
        assert result.games_played == 100
        assert result.home_runs == 20


class TestTeamStatsModel:
    def test_team_stats_fields(self, session, sample_team_stats):
        session.add(sample_team_stats)
        session.commit()

        result = session.query(TeamStats).filter_by(team_name="Atlanta Braves").first()
        assert result.wins == 92
        assert result.losses == 70
        assert result.team_era == 3.45
        assert result.division_rank == 1

    def test_record_calculation(self, session, sample_team_stats):
        session.add(sample_team_stats)
        session.commit()

        result = session.query(TeamStats).first()
        assert result.wins + result.losses == 162


class TestDbManager:
    def test_add_record(self, session):
        player = Player(name="DB Test", team="TST", position="SS")
        add_record(session, player)

        result = session.query(Player).filter_by(name="DB Test").first()
        assert result is not None

    def test_get_all_records(self, session):
        session.add(Player(name="P1", team="A", position="C"))
        session.add(Player(name="P2", team="B", position="1B"))
        session.commit()

        results = get_all_records(session, Player)
        assert len(results) == 2

    def test_update_record(self, session):
        player = Player(name="Updatable", team="TST", position="RF",
                        home_runs=10)
        session.add(player)
        session.commit()

        player.home_runs = 20
        update_record(session, player)

        result = session.query(Player).filter_by(name="Updatable").first()
        assert result.home_runs == 20
