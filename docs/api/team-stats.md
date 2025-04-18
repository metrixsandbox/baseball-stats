# Team Statistics API

## Get Team Stats

```http
GET /api/stats/team/{team_name}
```

Retrieve comprehensive statistics for a specific team.

### Parameters

| Parameter  | Type   | Description                          |
|------------|--------|--------------------------------------|
| team_name  | string | Full team name (e.g. "Atlanta Braves") |
| year       | number | Optional. Season year (default: 2025) |

### Response

```json
{
  "team_stats": {
    "name": "Atlanta Braves",
    "year": 2025,
    "record": "93-70",
    "batting": {
      "average": 0.267,
      "home_runs": 245,
      "runs_scored": 822
    },
    "pitching": {
      "era": 3.45,
      "strikeouts": 1524,
      "saves": 42,
      "whip": 1.18,
      "runs_allowed": 653
    },
    "division_rank": 1
  },
  "players": [
    {
      "name": "Ronald Acuña Jr.",
      "position": "RF",
      "batting_average": 0.325,
      "home_runs": 42,
      "runs_batted_in": 98
    }
  ],
  "recent_games": [
    {
      "date": "2025-04-17",
      "home_team": "ATL",
      "away_team": "PHI",
      "home_score": 7,
      "away_score": 3,
      "result": "W"
    }
  ]
}
```

## Get Team Report

```http
GET /api/report/team/{team_name}
```

Get a narrative report of team performance.

### Parameters

| Parameter  | Type   | Description                          |
|------------|--------|--------------------------------------|
| team_name  | string | Full team name (e.g. "Atlanta Braves") |
| year       | number | Optional. Season year (default: 2025) |

### Response

```json
{
  "summary": "The Atlanta Braves are currently 93-70 and ranked 1st in their division. They have won 4 of their last 5 games.",
  "offense": "The team is batting 0.267 with 245 home runs and 822 runs scored this season.",
  "pitching": "The pitching staff has posted a 3.45 ERA with 1524 strikeouts and a 1.18 WHIP. The bullpen has recorded 42 saves.",
  "recent_performance": "Recent games:\n2025-04-17: PHI 3 @ ATL 7\n2025-04-16: NYM 2 @ ATL 6"
}
```

## Update Team Game Results

```http
POST /api/games/update
```

Update database with new game results and statistics.

### Request Body

```json
{
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
}
```

### Response

```json
{
  "message": "Game data updated successfully",
  "game": {
    "date": "2025-04-17",
    "result": "PHI 3 @ ATL 7"
  }
}
```