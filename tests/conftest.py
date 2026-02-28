import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Player, Game, SeasonStats, TeamStats


@pytest.fixture
def engine():
    """Create an in-memory SQLite engine for testing."""
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture
def session(engine):
    """Create a new database session for each test."""
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()


@pytest.fixture
def sample_player():
    """Return a sample Player instance."""
    return Player(
        name="Mike Trout",
        team="LAA",
        position="CF",
        batting_average=0.296,
        home_runs=350,
        runs_batted_in=896,
    )


@pytest.fixture
def sample_game():
    """Return a sample Game instance."""
    return Game(
        date="2025-04-16",
        home_team="LAA",
        away_team="TEX",
        home_team_score=5,
        away_team_score=3,
    )


@pytest.fixture
def sample_team_stats():
    """Return a sample TeamStats instance."""
    return TeamStats(
        team_name="Atlanta Braves",
        year=2025,
        wins=92,
        losses=70,
        team_batting_avg=0.267,
        team_home_runs=245,
        team_runs_scored=815,
        team_runs_allowed=650,
        division_rank=1,
        team_era=3.45,
        team_strikeouts=1524,
        team_saves=42,
        team_whip=1.18,
    )


@pytest.fixture
def seeded_session(session, sample_player, sample_game, sample_team_stats):
    """Session pre-loaded with sample data for integration tests."""
    session.add(sample_player)
    session.flush()

    season_stats = SeasonStats(
        player_id=sample_player.id,
        year=2025,
        games_played=155,
        batting_average=0.296,
        home_runs=39,
        runs_batted_in=104,
    )
    session.add(season_stats)
    session.add(sample_game)
    session.add(sample_team_stats)
    session.commit()
    return session


@pytest.fixture
def app(engine):
    """Create a Flask test app wired to the test database."""
    from src.app import app as flask_app
    from src.database import db_manager

    # Monkey-patch db_manager to use the test engine/session
    original_engine = db_manager.engine
    original_session_class = db_manager.Session

    db_manager.engine = engine
    db_manager.Session = sessionmaker(bind=engine)

    flask_app.config["TESTING"] = True
    yield flask_app

    db_manager.engine = original_engine
    db_manager.Session = original_session_class


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()
