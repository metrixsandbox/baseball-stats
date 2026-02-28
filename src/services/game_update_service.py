from sqlalchemy import and_
from ..database.db_manager import get_session
from ..database.models import Player, Game, SeasonStats, TeamStats

class GameUpdateService:
    def __init__(self):
        self.session = get_session()

    def update_after_game(self, game_data):
        """
        Update database after a game is completed.
        
        Args:
            game_data: Dict containing:
                - date: Game date (YYYY-MM-DD)
                - home_team: Home team code (e.g., 'ATL')
                - away_team: Away team code
                - home_score: Home team score
                - away_score: Away team score
                - player_stats: List of player statistics for the game
        """
        try:
            # Add new game record
            game = Game(
                date=game_data['date'],
                home_team=game_data['home_team'],
                away_team=game_data['away_team'],
                home_team_score=game_data['home_score'],
                away_team_score=game_data['away_score']
            )
            self.session.add(game)
            
            # Update team records and stats
            self._update_team_stats(game_data)
            
            # Update player stats if provided
            if 'player_stats' in game_data:
                self._update_player_stats(game_data['player_stats'])
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error updating after game: {e}")
            return False
        finally:
            self.session.close()

    def _update_team_stats(self, game_data):
        """Update team statistics after a game."""
        home_team = game_data['home_team']
        away_team = game_data['away_team']
        home_won = game_data['home_score'] > game_data['away_score']
        
        # Update home team
        home_stats = self.session.query(TeamStats).filter(
            and_(
                TeamStats.team_name.like(f"%{home_team}%"),
                TeamStats.year == 2025
            )
        ).first()
        
        if home_stats:
            home_stats.wins = home_stats.wins + (1 if home_won else 0)
            home_stats.losses = home_stats.losses + (0 if home_won else 1)
            home_stats.team_runs_scored += game_data['home_score']
            home_stats.team_runs_allowed += game_data['away_score']
        
        # Update away team
        away_stats = self.session.query(TeamStats).filter(
            and_(
                TeamStats.team_name.like(f"%{away_team}%"),
                TeamStats.year == 2025
            )
        ).first()
        
        if away_stats:
            away_stats.wins = away_stats.wins + (0 if home_won else 1)
            away_stats.losses = away_stats.losses + (1 if home_won else 0)
            away_stats.team_runs_scored += game_data['away_score']
            away_stats.team_runs_allowed += game_data['home_score']

    def _update_player_stats(self, player_stats):
        """Update individual player statistics after a game."""
        for stat in player_stats:
            player = self.session.query(Player).filter_by(
                name=stat['name']
            ).first()
            
            if player:
                # Update season stats
                season_stat = self.session.query(SeasonStats).filter(
                    and_(
                        SeasonStats.player_id == player.id,
                        SeasonStats.year == 2025
                    )
                ).first()
                
                if season_stat:
                    # Update existing season stats
                    season_stat.games_played += 1
                    if 'at_bats' in stat and stat['at_bats'] > 0:
                        # Recalculate batting average
                        total_hits = (season_stat.batting_average * 
                                    (season_stat.games_played - 1) * 3.1) + stat['hits']
                        total_at_bats = ((season_stat.games_played - 1) * 3.1) + stat['at_bats']
                        season_stat.batting_average = total_hits / total_at_bats
                    season_stat.home_runs += stat.get('home_runs', 0)
                    season_stat.runs_batted_in += stat.get('rbi', 0)
                else:
                    # Create new season stats
                    new_stats = SeasonStats(
                        player_id=player.id,
                        year=2025,
                        games_played=1,
                        batting_average=stat.get('hits', 0) / stat.get('at_bats', 1) if stat.get('at_bats', 0) > 0 else 0.0,
                        home_runs=stat.get('home_runs', 0),
                        runs_batted_in=stat.get('rbi', 0)
                    )
                    self.session.add(new_stats)