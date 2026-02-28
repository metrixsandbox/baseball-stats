# Contributing

Contributions are welcome! This guide covers how to set up your development environment and submit changes.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork:

    ```bash
    git clone https://github.com/yourusername/baseball-stats.git
    cd baseball-stats
    ```

3. Create a virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. Initialize the database with sample data:

    ```bash
    python -m src.database.init_database
    ```

## Development Workflow

1. Create a branch for your feature or fix:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes.
3. Run the tests to make sure nothing is broken:

    ```bash
    pytest
    ```

4. Commit your changes with a clear message:

    ```bash
    git commit -m "Add your feature description"
    ```

5. Push to your fork and open a pull request.

## Running Tests

The test suite uses pytest with in-memory SQLite databases, so no external setup is needed:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_routes.py

# Run with coverage
pytest --cov=src tests/
```

## Project Structure

```
baseball-stats/
├── src/
│   ├── app.py              # Flask application entry point
│   ├── api/
│   │   └── routes.py       # API endpoint handlers
│   ├── database/
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── db_manager.py   # Database session management
│   │   └── init_database.py # Database initialization and sample data
│   ├── services/
│   │   ├── stats_service.py        # Statcast data fetching
│   │   ├── game_update_service.py  # Game result processing
│   │   └── metabase_service.py     # Metabase API integration
│   └── utils/
│       └── helpers.py
├── tests/
│   ├── conftest.py         # Shared test fixtures
│   ├── test_database.py
│   ├── test_stats.py
│   ├── test_routes.py
│   └── test_game_update_service.py
├── config/
│   └── config.py           # Environment configurations
└── docs/                   # MkDocs documentation
```

## Guidelines

- Write tests for new features. Place them in the `tests/` directory.
- Follow the existing code style and patterns.
- Keep commits focused — one logical change per commit.
- Update documentation if your change affects the API or setup process.

## Reporting Issues

Found a bug or have a feature request? [Open an issue](https://github.com/yourusername/baseball-stats/issues) with:

- A clear description of the problem or feature.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
