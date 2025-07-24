import unittest

from ArbitrageEngine import ArbitrageEngine


class EvaluateDealsTest(unittest.TestCase):
    def test_underpriced_detection(self):
        engine = ArbitrageEngine(search_terms=[])
        listings = [
            {"title": "cheap phone", "price": 50, "market_value": 200},
            {"title": "regular phone", "price": 100, "market_value": 150},
        ]
        deals = list(engine.evaluate_deals(listings))
        self.assertEqual(len(deals), 1)
        self.assertEqual(deals[0][0]["title"], "cheap phone")
        self.assertEqual(deals[0][1], 200)


if __name__ == "__main__":
    unittest.main()
