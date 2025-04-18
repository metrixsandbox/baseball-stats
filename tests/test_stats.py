import unittest
from src.services.stats_service import StatsService

class TestStatsService(unittest.TestCase):

    def setUp(self):
        self.service = StatsService()

    def test_fetch_stats(self):
        # Example test for fetching stats
        stats = self.service.fetch_stats('player_name')
        self.assertIsNotNone(stats)
        self.assertIn('player_name', stats)

    def test_process_stats(self):
        # Example test for processing stats
        raw_stats = {'player_name': 'player_name', 'home_runs': 10}
        processed = self.service.process_stats(raw_stats)
        self.assertEqual(processed['home_runs'], 10)

if __name__ == '__main__':
    unittest.main()