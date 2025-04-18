from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    position = Column(String, nullable=False)
    batting_average = Column(Float)
    home_runs = Column(Integer)
    runs_batted_in = Column(Integer)

class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)

class SeasonStats(Base):
    __tablename__ = 'season_stats'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    year = Column(Integer, nullable=False)
    games_played = Column(Integer)
    batting_average = Column(Float)
    home_runs = Column(Integer)
    runs_batted_in = Column(Integer)

class TeamStats(Base):
    __tablename__ = 'team_stats'
    
    id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    wins = Column(Integer)
    losses = Column(Integer)
    team_batting_avg = Column(Float)
    team_home_runs = Column(Integer)
    team_runs_scored = Column(Integer)
    team_runs_allowed = Column(Integer)
    division_rank = Column(Integer)
    team_era = Column(Float)
    team_strikeouts = Column(Integer)
    team_saves = Column(Integer)
    team_whip = Column(Float)