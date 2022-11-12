import unittest
from fill_server import StockTicker, StockTickerGenerator


class FillServerTest(unittest.TestCase):
    def test_generate_stock_attributes(self):
        stock_ticker1 = StockTickerGenerator.generate_stock_attributes("stock1")
        stock_ticker2 = StockTickerGenerator.generate_stock_attributes("stock1")
        self.assertNotEqual(stock_ticker1, stock_ticker2)

    def test_stock_ticker_serialize(self):
        stock_ticker = StockTicker(name="stock1", price=11.10, quantity=100)
        self.assertEqual(
            stock_ticker.serialize(),
            '{"name": "stock1", "price": 11.1, "quantity": 100}',
        )


if __name__ == "__main__":
    unittest.main()
