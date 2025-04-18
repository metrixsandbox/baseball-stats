from dotenv import load_dotenv
import os
from src.database.db_manager import init_db, engine, get_session
from src.database.models import Player, Game, SeasonStats, TeamStats, Base

load_dotenv()

def clear_database():
    """Clear all data from the database"""
    session = get_session()
    session.query(SeasonStats).delete()
    session.query(Player).delete()
    session.query(Game).delete()
    session.query(TeamStats).delete()
    session.commit()

def create_sample_data():
    session = get_session()
    
    # Clear existing data
    clear_database()
    
    # Add sample player
    player = Player(
        name="Mike Trout",
        team="LAA",
        position="CF",
        batting_average=0.296,
        home_runs=350,
        runs_batted_in=896
    )
    session.add(player)
    
    # Add sample game
    game = Game(
        date="2025-04-16",
        home_team="LAA",
        away_team="TEX",
        home_team_score=5,
        away_team_score=3
    )
    session.add(game)
    
    # Add sample season stats
    stats = SeasonStats(
        player_id=1,
        year=2024,
        games_played=162,
        batting_average=0.298,
        home_runs=39,
        runs_batted_in=104
    )
    session.add(stats)
    
    # Add Atlanta Braves 2025 team stats with detailed metrics
    braves_stats = TeamStats(
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
        team_whip=1.18
    )
    session.add(braves_stats)
    
    # Add expanded roster of Braves players
    braves_players = [
        Player(
            name="Ronald Acuña Jr.",
            team="ATL",
            position="RF",
            batting_average=0.325,
            home_runs=42,
            runs_batted_in=98
        ),
        Player(
            name="Matt Olson",
            team="ATL",
            position="1B",
            batting_average=0.283,
            home_runs=48,
            runs_batted_in=115
        ),
        Player(
            name="Austin Riley",
            team="ATL",
            position="3B",
            batting_average=0.278,
            home_runs=35,
            runs_batted_in=92
        ),
        Player(
            name="Spencer Strider",
            team="ATL",
            position="SP",
            batting_average=0.000,
            home_runs=0,
            runs_batted_in=0
        ),
        Player(
            name="Michael Harris II",
            team="ATL",
            position="CF",
            batting_average=0.292,
            home_runs=22,
            runs_batted_in=78
        ),
        Player(
            name="Ozzie Albies",
            team="ATL",
            position="2B",
            batting_average=0.285,
            home_runs=28,
            runs_batted_in=95
        ),
        Player(
            name="Max Fried",
            team="ATL",
            position="SP",
            batting_average=0.122,
            home_runs=0,
            runs_batted_in=3
        ),
        Player(
            name="Charlie Morton",
            team="ATL",
            position="SP",
            batting_average=0.108,
            home_runs=0,
            runs_batted_in=2
        ),
        Player(
            name="Raisel Iglesias",
            team="ATL",
            position="RP",
            batting_average=0.000,
            home_runs=0,
            runs_batted_in=0
        )
    ]
    
    for player in braves_players:
        session.add(player)
        
        # Add 2025 season stats for each Braves player
        if player.name == "Ronald Acuña Jr.":
            season_stats = SeasonStats(
                player_id=len(session.query(Player).all()),
                year=2025,
                games_played=155,
                batting_average=0.325,
                home_runs=42,
                runs_batted_in=98
            )
            session.add(season_stats)
        elif player.name == "Matt Olson":
            season_stats = SeasonStats(
                player_id=len(session.query(Player).all()),
                year=2025,
                games_played=162,
                batting_average=0.283,
                home_runs=48,
                runs_batted_in=115
            )
            session.add(season_stats)
    
    # Add key Braves games from 2025
    braves_games = [
        Game(
            date="2025-04-16",
            home_team="ATL",
            away_team="NYM",
            home_team_score=6,
            away_team_score=2
        ),
        Game(
            date="2025-04-15",
            home_team="ATL",
            away_team="NYM",
            home_team_score=8,
            away_team_score=3
        ),
        Game(
            date="2025-04-14",
            home_team="ATL",
            away_team="NYM",
            home_team_score=4,
            away_team_score=5
        ),
        Game(
            date="2025-04-12",
            home_team="MIA",
            away_team="ATL",
            home_team_score=2,
            away_team_score=7
        ),
        Game(
            date="2025-04-11",
            home_team="MIA",
            away_team="ATL",
            home_team_score=1,
            away_team_score=3
        )
    ]
    
    for game in braves_games:
        session.add(game)
    
    session.commit()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Creating sample data...")
    create_sample_data()
    print("Database initialized successfully!")