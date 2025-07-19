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


class FetchListingsDedupTest(unittest.TestCase):
    def test_duplicate_urls_ignored(self):
        engine = ArbitrageEngine(search_terms=[], marketplaces=["ebay"])

        sample_listing = {
            "title": "item",
            "price": 10,
            "url": "http://example.com/item",
        }
        returned = [sample_listing, sample_listing]

        from unittest import mock

        with mock.patch.object(engine, "query_ebay", return_value=returned):
            first = list(engine.fetch_listings())
            self.assertEqual(len(first), 1)

            second = list(engine.fetch_listings())
            self.assertEqual(len(second), 0)

            engine.prune_seen_urls()

            third = list(engine.fetch_listings())
            self.assertEqual(len(third), 1)


if __name__ == "__main__":
    unittest.main()
