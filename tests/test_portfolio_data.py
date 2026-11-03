import unittest
from backend.stock_data import stock_manager

class TestPortfolioData(unittest.TestCase):
    def test_portfolio_stock_count(self):
        stocks = stock_manager.get_all_portfolio_stocks()
        self.assertEqual(len(stocks), 18, "Portfolio should contain 18 NSE-listed companies")

    def test_volume_multiple_calculation(self):
        wipro = stock_manager.get_stock("WIPRO")
        self.assertIsNotNone(wipro)
        expected_mult = round(wipro.volume / wipro.avg_volume_20d, 2)
        self.assertEqual(wipro.volume_multiple, expected_mult)
        self.assertGreater(wipro.volume_multiple, 2.0, "WIPRO volume multiple should exceed 2.0x threshold")

    def test_portfolio_summary_totals(self):
        summary = stock_manager.get_portfolio_summary()
        self.assertGreater(summary.total_value_inr, 0)
        self.assertEqual(len(summary.top_gainers), 4)
        self.assertEqual(len(summary.top_losers), 4)

    def test_adhoc_ticker_lookup(self):
        zomato = stock_manager.get_stock("ZOMATO")
        self.assertIsNotNone(zomato)
        self.assertEqual(zomato.ticker, "ZOMATO")
        self.assertGreater(zomato.price, 0)

if __name__ == '__main__':
    unittest.main()
