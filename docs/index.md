# Baseball Stats API Documentation

Welcome to the Baseball Stats API documentation! This API provides comprehensive baseball statistics tracking with real-time updates, player stats, and team analytics.

## Overview

The Baseball Stats API is a powerful tool for tracking and analyzing baseball statistics, featuring:

- Live game statistics tracking
- Team and player performance analytics
- Automated database updates
- Metabase integration for data visualization
- RESTful API endpoints
- Support for the 2025 MLB season

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [API Reference](api/team-stats.md)
- [Metabase Setup](visualization/metabase-setup.md)
- [Contributing Guide](contributing.md)

## Example Usage

```python
import requests

# Get team stats
response = requests.get('http://localhost:5000/api/stats/team/Atlanta%20Braves')
stats = response.json()

# Update game results
game_data = {
    "date": "2025-04-17",
    "home_team": "ATL",
    "away_team": "PHI",
    "home_score": 7,
    "away_score": 3
}
response = requests.post('http://localhost:5000/api/games/update', json=game_data)
```

## Support

If you need help or have questions:

1. Check the [documentation](getting-started/installation.md)
2. Open an [issue](https://github.com/yourusername/baseball-stats/issues)
3. Submit a [pull request](https://github.com/yourusername/baseball-stats/pulls)