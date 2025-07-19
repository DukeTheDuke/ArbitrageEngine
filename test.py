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


class InitMarketplacesTest(unittest.TestCase):
    def test_custom_marketplaces(self):
        engine = ArbitrageEngine(search_terms=[], marketplaces=["ebay"])
        self.assertEqual(engine.marketplaces, ["ebay"])


class PriceExtractionTest(unittest.TestCase):
    def test_extract_first_price(self):
        engine = ArbitrageEngine(search_terms=[])
        html = "<div><span>$19.99</span></div>"
        self.assertEqual(engine._extract_first_price(html), 19.99)

    def test_query_uses_extracted_price(self):
        from unittest import mock

        engine = ArbitrageEngine(search_terms=["phone"])
        fake_response = mock.Mock()
        fake_response.text = "<span>$42</span>"
        fake_response.raise_for_status.return_value = None

        with mock.patch("ArbitrageEngine.requests.get", return_value=fake_response):
            listings = engine.query_ebay()

        self.assertEqual(listings[0]["price"], 42.0)


class CLIMarketplacesTest(unittest.TestCase):
    def test_cli_parses_marketplaces(self):
        import sys
        from unittest import mock

        argv = [
            "prog",
            "item",
            "--marketplaces",
            "ebay,craigslist",
            "--marketplaces",
            "facebook",
        ]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                _, kwargs = AE.call_args
                self.assertEqual(
                    kwargs.get("marketplaces"),
                    ["ebay", "craigslist", "facebook"],
                )


if __name__ == "__main__":
    unittest.main()
