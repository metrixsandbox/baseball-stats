# Installation

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- Java Runtime Environment (optional, for Metabase)

## Clone the Repository

```bash
git clone https://github.com/yourusername/baseball-stats.git
cd baseball-stats
```

## Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Configure Environment Variables

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

See the [Configuration](configuration.md) guide for details on each variable.

## Initialize the Database

```bash
python -m src.database.init_database
```

This creates the SQLite database (`baseball_stats.db`) and populates it with sample data including the 2025 Atlanta Braves roster and recent games.

!!! warning
    Running `init_database` drops and recreates all tables. Do not run this on a database with data you want to keep.

## Start the API Server

```bash
python -m src.app
```

The API will be available at `http://localhost:5000`.

## Verify the Installation

```bash
curl http://localhost:5000/
# Expected: "Welcome to the Baseball Stats API!"

curl http://localhost:5000/api/players
# Expected: JSON array of players
```

## Optional: Start Metabase

If you want data visualization dashboards, see the [Metabase Setup](../visualization/metabase-setup.md) guide.

## Running Tests

```bash
pytest
```

All tests use an in-memory SQLite database, so no external setup is required.
