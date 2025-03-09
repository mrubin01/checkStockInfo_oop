import unittest
from Asset import Equity


class TestEquity(unittest.TestCase):
    def setUp(self):
        print("\nRunning setUp method...")
        self.equity1 = Equity("KSFIBSV", "NYSE")
        self.equity2 = Equity("")
        self.equity3 = Equity("CCLDO")
        self.equity4 = Equity("CCLDO", "NASDAQ")

    def tearDown(self):
        print("Running tearDown method...")

    def test_get_info(self):
        print("Running test_get_info...")
        self.assertEqual(self.equity1.get_info(), {})
        self.assertEqual(self.equity2.get_info(), {})

    def test_get_yearly_dividend(self):
        print("Running test_get_yearly_dividend...")
        self.assertEqual(self.equity1.get_yearly_dividend(2024), -999999)
        self.assertEqual(self.equity3.get_yearly_dividend(2024), 0.0)
        self.assertEqual(self.equity4.get_yearly_dividend(2023), 2.184)

    def test_get_ytd_dividend(self):
        print("Running test_get_ytd_dividend...")
        self.assertEqual(self.equity1.get_ytd_dividend(2025, 3, 1), -999999)
        self.assertEqual(self.equity3.get_ytd_dividend(2025, 3, 1), 0.364)
        self.assertEqual(self.equity4.get_ytd_dividend(2025, 3, 1), 0.364)

    def test_get_all_dividends(self):
        print("Running test_get_all_dividends...")
        self.assertEqual(self.equity1.get_all_dividends(), 0)
        self.assertEqual(self.equity2.get_all_dividends(), 0)


if __name__ == "__main__":
    unittest.main()
