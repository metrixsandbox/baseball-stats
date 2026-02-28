# Player Statistics API

## List All Players

```http
GET /api/players
```

Returns all players in the database with their current statistics.

### Response

```json
[
  {
    "id": 1,
    "name": "Ronald Acuña Jr.",
    "team": "ATL",
    "position": "RF",
    "batting_average": 0.325,
    "home_runs": 42,
    "runs_batted_in": 98
  },
  {
    "id": 2,
    "name": "Matt Olson",
    "team": "ATL",
    "position": "1B",
    "batting_average": 0.283,
    "home_runs": 48,
    "runs_batted_in": 115
  }
]
```

### Example

```bash
curl http://localhost:5000/api/players
```

## Get Player Season Stats

```http
GET /api/stats/player/{player_id}
```

Returns season-by-season statistics for a specific player.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `player_id` | integer | The player's database ID (from the `/api/players` response) |

### Response

```json
[
  {
    "year": 2025,
    "games_played": 155,
    "batting_average": 0.325,
    "home_runs": 42,
    "runs_batted_in": 98
  }
]
```

Returns an empty array `[]` if the player has no recorded season stats.

### Example

```bash
curl http://localhost:5000/api/stats/player/1
```

## Get Latest Statcast Data

```http
GET /api/stats/latest
```

Fetches the last 7 days of pitch-level data from the MLB Statcast API via PyBaseball.

### Response

Returns an array of daily player statistics aggregated from Statcast data:

```json
[
  {
    "player_name": "Ronald Acuña Jr.",
    "game_date": "2025-04-16",
    "launch_speed": 95.4,
    "hit_distance_sc": 320.5,
    "events": {"single": 1, "home_run": 1}
  }
]
```

!!! note
    This endpoint calls the external Statcast API and may take several seconds to respond. It requires an active internet connection.

### Example

```bash
curl http://localhost:5000/api/stats/latest
```
