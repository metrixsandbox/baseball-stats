# Configuration

The application is configured through environment variables, loaded from a `.env` file at the project root.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URI` | `sqlite:///baseball_stats.db` | SQLAlchemy database connection string |
| `API_KEY` | `your_api_key_here` | API key for authentication (reserved for future use) |
| `METABASE_URL` | `http://localhost:3000` | URL where Metabase is running |
| `METABASE_USER` | `admin@baseball.stats` | Metabase admin username |
| `METABASE_PASSWORD` | `changeme` | Metabase admin password |

## Configuration Classes

The application supports three configuration profiles defined in `config/config.py`:

### Development (default)

```python
class DevelopmentConfig(Config):
    DEBUG = True
```

Uses the default SQLite database with debug mode enabled.

### Testing

```python
class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///test_baseball_stats.db'
```

Uses a separate test database. The test suite itself uses in-memory SQLite via fixtures in `conftest.py`.

### Production

```python
class ProductionConfig(Config):
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///baseball_stats.db')
```

Reads the database URI from the environment. Set `DATABASE_URI` to point to your production database (e.g., PostgreSQL).

## Database

The default database is SQLite, stored as `baseball_stats.db` in the project root. SQLAlchemy supports other backends — to use PostgreSQL, for example:

```
DATABASE_URI=postgresql://user:password@localhost:5432/baseball_stats
```

You would also need to install the appropriate driver (e.g., `psycopg2`).
