import json

from src.database.models import Player, Game, TeamStats, SeasonStats


class TestHomeRoute:
    def test_home(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"Baseball Stats API" in resp.data


class TestGetPlayers:
    def test_empty_database(self, client):
        resp = client.get("/api/players")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_returns_players(self, client, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as sess:
            sess.add(Player(name="Test", team="TST", position="CF",
                            batting_average=0.300, home_runs=10,
                            runs_batted_in=50))
            sess.commit()

        resp = client.get("/api/players")
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "Test"
        assert data[0]["batting_average"] == 0.300


class TestGetPlayerStats:
    def test_no_stats(self, client):
        resp = client.get("/api/stats/player/999")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_returns_season_stats(self, client, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as sess:
            player = Player(name="Slugger", team="TST", position="DH")
            sess.add(player)
            sess.flush()
            sess.add(SeasonStats(
                player_id=player.id, year=2025, games_played=100,
                batting_average=0.310, home_runs=30, runs_batted_in=80,
            ))
            sess.commit()
            pid = player.id

        resp = client.get(f"/api/stats/player/{pid}")
        data = resp.get_json()
        assert len(data) == 1
        assert data[0]["year"] == 2025
        assert data[0]["home_runs"] == 30


class TestGetTeamStats:
    def test_team_not_found(self, client):
        resp = client.get("/api/stats/team/Nonexistent")
        assert resp.status_code == 404

    def test_returns_team_stats(self, client, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as sess:
            sess.add(TeamStats(
                team_name="Atlanta Braves", year=2025, wins=92, losses=70,
                team_batting_avg=0.267, team_home_runs=245,
                team_runs_scored=815, team_runs_allowed=650,
                division_rank=1, team_era=3.45, team_strikeouts=1524,
                team_saves=42, team_whip=1.18,
            ))
            sess.add(Player(name="Acuna", team="ATL", position="RF",
                            batting_average=0.325, home_runs=42,
                            runs_batted_in=98))
            sess.add(Game(date="2025-04-16", home_team="ATL",
                          away_team="NYM", home_team_score=6,
                          away_team_score=2))
            sess.commit()

        resp = client.get("/api/stats/team/Atlanta Braves")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["team_stats"]["record"] == "92-70"
        assert len(data["players"]) == 1
        assert len(data["recent_games"]) == 1
        assert data["recent_games"][0]["result"] == "W"


class TestGetTeamReport:
    def test_report_not_found(self, client):
        resp = client.get("/api/report/team/Nonexistent")
        assert resp.status_code == 404

    def test_report_content(self, client, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as sess:
            sess.add(TeamStats(
                team_name="Atlanta Braves", year=2025, wins=92, losses=70,
                team_batting_avg=0.267, team_home_runs=245,
                team_runs_scored=815, team_runs_allowed=650,
                division_rank=1, team_era=3.45, team_strikeouts=1524,
                team_saves=42, team_whip=1.18,
            ))
            sess.commit()

        resp = client.get("/api/report/team/Atlanta Braves")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "92-70" in data["summary"]
        assert "3.45" in data["pitching"]
        assert "0.267" in data["offense"]


class TestUpdateGame:
    def test_missing_fields(self, client):
        resp = client.post("/api/games/update",
                           data=json.dumps({"date": "2025-04-16"}),
                           content_type="application/json")
        assert resp.status_code == 400
        assert "Missing required fields" in resp.get_json()["error"]

    def test_successful_update(self, client, engine):
        from sqlalchemy.orm import Session
        with Session(engine) as sess:
            sess.add(TeamStats(
                team_name="Atlanta Braves", year=2025, wins=92, losses=70,
                team_batting_avg=0.267, team_home_runs=245,
                team_runs_scored=815, team_runs_allowed=650,
                division_rank=1, team_era=3.45, team_strikeouts=1524,
                team_saves=42, team_whip=1.18,
            ))
            sess.commit()

        payload = {
            "date": "2025-04-17",
            "home_team": "ATL",
            "away_team": "PHI",
            "home_score": 7,
            "away_score": 3,
        }
        resp = client.post("/api/games/update",
                           data=json.dumps(payload),
                           content_type="application/json")
        assert resp.status_code == 200
        assert "successfully" in resp.get_json()["message"]
