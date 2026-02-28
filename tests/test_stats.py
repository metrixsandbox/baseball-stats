import pandas as pd
from unittest.mock import patch

from src.services.stats_service import fetch_stats, process_stats


class TestFetchStats:
    @patch("src.services.stats_service.statcast")
    def test_fetch_stats_returns_dataframe(self, mock_statcast):
        mock_statcast.return_value = pd.DataFrame({"player_name": ["Test"]})
        result = fetch_stats("2025-04-10", "2025-04-16")
        assert isinstance(result, pd.DataFrame)
        mock_statcast.assert_called_once_with(
            start_dt="2025-04-10", end_dt="2025-04-16"
        )

    @patch("src.services.stats_service.statcast")
    def test_fetch_stats_passes_dates(self, mock_statcast):
        mock_statcast.return_value = pd.DataFrame()
        fetch_stats("2025-01-01", "2025-01-07")
        mock_statcast.assert_called_once_with(
            start_dt="2025-01-01", end_dt="2025-01-07"
        )


class TestProcessStats:
    def test_empty_dataframe(self):
        result = process_stats(pd.DataFrame())
        assert result.empty

    def test_none_input(self):
        result = process_stats(None)
        assert result.empty

    def test_processes_valid_data(self):
        data = pd.DataFrame({
            "player_name": ["Player A", "Player A", "Player B"],
            "game_date": ["2025-04-16", "2025-04-16", "2025-04-16"],
            "events": ["single", "home_run", "strikeout"],
            "hit_distance_sc": [150.0, 420.0, 0.0],
            "launch_speed": [95.0, 110.0, 85.0],
            "home_score": [3, 3, 3],
            "away_score": [1, 1, 1],
        })

        result = process_stats(data)
        assert not result.empty
        assert "player_name" in result.columns
        assert "game_date" in result.columns
        assert len(result) == 2  # two players grouped

    def test_missing_columns_handled(self):
        """Columns not present in the DataFrame are simply skipped."""
        data = pd.DataFrame({
            "player_name": ["A"],
            "game_date": ["2025-04-16"],
            "events": ["single"],
            "launch_speed": [95.0],
            "hit_distance_sc": [150.0],
        })
        result = process_stats(data)
        assert not result.empty
