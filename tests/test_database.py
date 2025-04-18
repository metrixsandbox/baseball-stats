import unittest
from src.database.db_manager import add_record, get_record
from src.database.models import BaseballStat

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Set up a test database or mock database connection
        self.test_stat = BaseballStat(player_name="Test Player", home_runs=10, batting_average=0.300)

    def test_add_record(self):
        result = add_record(self.test_stat)
        self.assertTrue(result)

    def test_get_record(self):
        add_record(self.test_stat)
        result = get_record(self.test_stat.player_name)
        self.assertEqual(result.player_name, self.test_stat.player_name)
        self.assertEqual(result.home_runs, self.test_stat.home_runs)
        self.assertEqual(result.batting_average, self.test_stat.batting_average)

    def tearDown(self):
        # Clean up the test database or mock database connection
        pass

if __name__ == '__main__':
    unittest.main()