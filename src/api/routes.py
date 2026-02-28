from flask import Blueprint, jsonify, request
from ..services.stats_service import fetch_stats, process_stats
from ..services.metabase_service import MetabaseService
from ..services.game_update_service import GameUpdateService
from ..database.db_manager import get_session
from ..database.models import Player, Game, SeasonStats, TeamStats
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats/latest', methods=['GET'])
def get_latest_stats():
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        stats = fetch_stats(start_date, end_date)
        processed_stats = process_stats(stats)
        return jsonify(processed_stats.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/players', methods=['GET'])
def get_players():
    session = get_session()
    try:
        players = session.query(Player).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'team': p.team,
            'position': p.position,
            'batting_average': p.batting_average,
            'home_runs': p.home_runs,
            'runs_batted_in': p.runs_batted_in
        } for p in players]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api_bp.route('/stats/player/<int:player_id>', methods=['GET'])
def get_player_stats(player_id):
    session = get_session()
    try:
        stats = session.query(SeasonStats).filter_by(player_id=player_id).all()
        return jsonify([{
            'year': s.year,
            'games_played': s.games_played,
            'batting_average': s.batting_average,
            'home_runs': s.home_runs,
            'runs_batted_in': s.runs_batted_in
        } for s in stats]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api_bp.route('/stats/team/<team_name>', methods=['GET'])
def get_team_stats(team_name):
    session = get_session()
    try:
        year = request.args.get('year', 2025)  # Default to 2025

        # Get team stats
        team_stats = session.query(TeamStats).filter_by(
            team_name=team_name,
            year=year
        ).first()

        if not team_stats:
            return jsonify({"error": "Team stats not found"}), 404

        # Get team players
        players = session.query(Player).filter_by(team=team_name[:3].upper()).all()

        # Get recent games
        recent_games = session.query(Game).filter(
            ((Game.home_team == team_name[:3].upper()) |
             (Game.away_team == team_name[:3].upper()))
        ).order_by(Game.date.desc()).limit(5).all()

        return jsonify({
            "team_stats": {
                "name": team_stats.team_name,
                "year": team_stats.year,
                "record": f"{team_stats.wins}-{team_stats.losses}",
                "batting": {
                    "average": team_stats.team_batting_avg,
                    "home_runs": team_stats.team_home_runs,
                    "runs_scored": team_stats.team_runs_scored
                },
                "pitching": {
                    "era": team_stats.team_era,
                    "strikeouts": team_stats.team_strikeouts,
                    "saves": team_stats.team_saves,
                    "whip": team_stats.team_whip,
                    "runs_allowed": team_stats.team_runs_allowed
                },
                "division_rank": team_stats.division_rank
            },
            "players": [{
                "name": p.name,
                "position": p.position,
                "batting_average": p.batting_average,
                "home_runs": p.home_runs,
                "runs_batted_in": p.runs_batted_in
            } for p in players],
            "recent_games": [{
                "date": game.date,
                "home_team": game.home_team,
                "away_team": game.away_team,
                "home_score": game.home_team_score,
                "away_score": game.away_team_score,
                "result": "W" if
                    (game.home_team == team_name[:3].upper() and game.home_team_score > game.away_team_score) or
                    (game.away_team == team_name[:3].upper() and game.away_team_score > game.home_team_score)
                    else "L"
            } for game in recent_games]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api_bp.route('/dashboard/braves', methods=['POST'])
def create_braves_dashboard():
    try:
        metabase = MetabaseService()
        dashboard_id = metabase.create_braves_dashboard()

        if dashboard_id:
            return jsonify({
                "message": "Braves dashboard created successfully",
                "dashboard_id": dashboard_id,
                "dashboard_url": f"{metabase.metabase_url}/dashboard/{dashboard_id}"
            }), 201
        else:
            return jsonify({"error": "Failed to create dashboard"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/report/team/<team_name>', methods=['GET'])
def get_team_report(team_name):
    session = get_session()
    try:
        year = request.args.get('year', 2025)

        # Get team stats
        team_stats = session.query(TeamStats).filter_by(
            team_name=team_name,
            year=year
        ).first()

        if not team_stats:
            return jsonify({"error": "Team stats not found"}), 404

        # Get recent games
        recent_games = session.query(Game).filter(
            ((Game.home_team == team_name[:3].upper()) |
             (Game.away_team == team_name[:3].upper()))
        ).order_by(Game.date.desc()).limit(5).all()

        # Calculate recent performance
        recent_wins = sum(1 for g in recent_games if
            (g.home_team == team_name[:3].upper() and g.home_team_score > g.away_team_score) or
            (g.away_team == team_name[:3].upper() and g.away_team_score > g.home_team_score))

        # Generate narrative report
        report = {
            "summary": f"The {team_stats.team_name} are currently {team_stats.wins}-{team_stats.losses} " +
                      f"and ranked {team_stats.division_rank}{'st' if team_stats.division_rank == 1 else 'th'} in their division. " +
                      f"They have won {recent_wins} of their last {len(recent_games)} games.",

            "offense": f"The team is batting {team_stats.team_batting_avg:.3f} with {team_stats.team_home_runs} home runs " +
                      f"and {team_stats.team_runs_scored} runs scored this season.",

            "pitching": f"The pitching staff has posted a {team_stats.team_era:.2f} ERA with {team_stats.team_strikeouts} " +
                      f"strikeouts and a {team_stats.team_whip:.2f} WHIP. The bullpen has recorded {team_stats.team_saves} saves.",

            "recent_performance": "Recent games:\n" + "\n".join([
                f"{g.date}: {g.away_team} {g.away_team_score} @ {g.home_team} {g.home_team_score}"
                for g in recent_games
            ])
        }

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api_bp.route('/games/update', methods=['POST'])
def update_game():
    try:
        game_data = request.json
        required_fields = ['date', 'home_team', 'away_team', 'home_score', 'away_score']

        # Validate required fields
        if not all(field in game_data for field in required_fields):
            return jsonify({
                "error": "Missing required fields",
                "required": required_fields
            }), 400

        # Update database with game results
        update_service = GameUpdateService()
        success = update_service.update_after_game(game_data)

        if success:
            return jsonify({
                "message": "Game data updated successfully",
                "game": {
                    "date": game_data['date'],
                    "result": f"{game_data['away_team']} {game_data['away_score']} @ {game_data['home_team']} {game_data['home_score']}"
                }
            }), 200
        else:
            return jsonify({"error": "Failed to update game data"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
