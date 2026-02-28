# Metabase Setup

[Metabase](https://www.metabase.com/) provides interactive dashboards and visualizations for your baseball statistics data.

## Prerequisites

- Docker (recommended) or Java Runtime Environment
- A populated `baseball_stats.db` database

## Option 1: Docker (Recommended)

The project includes a `docker-compose.yml` that sets up Metabase with your database:

```bash
docker-compose up -d
```

This starts Metabase on port 3000 with your SQLite database mounted.

## Option 2: Standalone JAR

If you prefer to run Metabase directly:

```bash
java -jar metabase.jar
```

The project includes database driver plugins in the `plugins/` directory for various backends (SQLite, PostgreSQL, MySQL, etc.).

## Initial Configuration

1. Open Metabase at [http://localhost:3000](http://localhost:3000).
2. Complete the setup wizard:
    - Create an admin account.
    - When prompted for a database, select **SQLite** and point to `/baseball_stats.db` (Docker) or `./baseball_stats.db` (standalone).
3. Metabase will scan your database tables automatically.

## Environment Variables

Configure Metabase connection details in your `.env` file:

```
METABASE_URL=http://localhost:3000
METABASE_USER=admin@baseball.stats
METABASE_PASSWORD=changeme
```

These are used by the API's Metabase integration to create dashboards programmatically.

## Create a Dashboard via the API

The API includes an endpoint to create a pre-configured Braves dashboard:

```bash
curl -X POST http://localhost:5000/api/dashboard/braves
```

Response:

```json
{
  "message": "Braves dashboard created successfully",
  "dashboard_id": 1,
  "dashboard_url": "http://localhost:3000/dashboard/1"
}
```

## Available Database Tables

Once connected, Metabase will expose these tables for building queries and dashboards:

| Table | Description |
|-------|-------------|
| `players` | Player roster with name, team, position, and batting stats |
| `games` | Game results with dates, teams, and scores |
| `season_stats` | Per-player season statistics (linked to players via `player_id`) |
| `team_stats` | Team-level season statistics including batting and pitching |

See the [Dashboards](dashboards.md) guide for ideas on what to build.
