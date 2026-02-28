# Game Updates API

## Update Game Results

```http
POST /api/games/update
```

Record a completed game and update team and player statistics.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | string | Yes | Game date in `YYYY-MM-DD` format |
| `home_team` | string | Yes | Home team code (e.g., `"ATL"`) |
| `away_team` | string | Yes | Away team code (e.g., `"PHI"`) |
| `home_score` | integer | Yes | Home team final score |
| `away_score` | integer | Yes | Away team final score |
| `player_stats` | array | No | Individual player statistics for the game |

### Player Stats Object

Each entry in the `player_stats` array:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Player's full name (must match database) |
| `at_bats` | integer | No | Number of at-bats |
| `hits` | integer | No | Number of hits |
| `home_runs` | integer | No | Number of home runs |
| `rbi` | integer | No | Runs batted in |

### Example Request

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

### Success Response (200)

```json
{
  "message": "Game data updated successfully",
  "game": {
    "date": "2025-04-17",
    "result": "PHI 3 @ ATL 7"
  }
}
```

### Error Response (400) - Missing Fields

```json
{
  "error": "Missing required fields",
  "required": ["date", "home_team", "away_team", "home_score", "away_score"]
}
```

### Error Response (500) - Update Failed

```json
{
  "error": "Failed to update game data"
}
```

## What Gets Updated

When a game is recorded, the following updates happen automatically:

1. **Game record** - A new entry is added to the games table.
2. **Team stats** - Wins/losses, runs scored, and runs allowed are updated for both teams (matched by team code in the team name).
3. **Player stats** - If `player_stats` is provided, each player's season statistics are updated:
    - Games played is incremented.
    - Batting average is recalculated.
    - Home runs and RBIs are added to season totals.
    - If no season stats exist for the player, a new record is created.

All updates happen in a single database transaction. If any step fails, all changes are rolled back.
