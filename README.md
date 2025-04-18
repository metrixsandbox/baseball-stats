# README.md

# Baseball Stats API

A comprehensive baseball statistics tracking system with real-time game updates, player stats, and team analytics. Features integration with Metabase for data visualization.

## Features

- Live game statistics tracking and updates
- Team and player performance analytics
- RESTful API for accessing baseball statistics
- Metabase integration for data visualization
- Automated database updates after each game
- Detailed player and team statistics
- Season-long performance tracking
- Support for the 2025 MLB season

## Tech Stack

- Python 3.11+
- Flask for REST API
- SQLAlchemy for database management
- Metabase for data visualization
- PyBaseball for baseball statistics
- SQLite database (configurable for other databases)

## API Endpoints

### Team Statistics
- `GET /api/stats/team/<team_name>` - Get comprehensive team statistics
- `GET /api/report/team/<team_name>` - Get narrative team report
- `POST /api/games/update` - Update game results and statistics

### Player Statistics
- `GET /api/players` - List all players
- `GET /api/stats/player/<player_id>` - Get player statistics
- `GET /api/stats/latest` - Get latest player statistics

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/baseball-stats.git
   cd baseball-stats
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -m src.database.init_database
   ```

5. Start the API server:
   ```bash
   python -m src.app
   ```

6. Start Metabase (optional):
   ```bash
   java -jar metabase.jar
   ```

## Using the API

### Add a New Game Result
```bash
curl -X POST http://localhost:5000/api/games/update \
-H "Content-Type: application/json" \
-d '{
    "date": "2025-04-17",
    "home_team": "ATL",
    "away_team": "PHI",
    "home_score": 7,
    "away_score": 3,
    "player_stats": [
        {
            "name": "Ronald Acuña Jr.",
            "at_bats": 4,
            "hits": 2,
            "home_runs": 1,
            "rbi": 3
        }
    ]
}'
```

### Get Team Statistics
```bash
curl http://localhost:5000/api/stats/team/Atlanta%20Braves
```

## Data Visualization

The project includes Metabase integration for data visualization. After starting Metabase:

1. Access Metabase at http://localhost:3000
2. Complete the initial setup
3. Connect to the baseball_stats.db database
4. Access pre-built dashboards or create custom visualizations

## Development

### Running Tests
```bash
pytest
```

### Adding New Features
1. Create a new branch for your feature
2. Write tests in the `tests/` directory
3. Implement your feature
4. Ensure all tests pass
5. Submit a pull request

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PyBaseball library for baseball statistics
- Metabase for data visualization
- The baseball statistics community for inspiration and support