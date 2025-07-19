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


class ConfigMergeTest(unittest.TestCase):
    def test_cli_overrides_config(self):
        import sys
        import json
        from tempfile import NamedTemporaryFile
        from unittest import mock

        cfg = {
            "search_terms": ["fromcfg"],
            "marketplaces": ["ebay"],
            "refresh_interval": 30,
            "deal_threshold": 0.4,
        }
        with NamedTemporaryFile("w", delete=False) as tmp:
            json.dump(cfg, tmp)
            path = tmp.name

        argv = [
            "prog",
            "cli-term",
            "--config",
            path,
            "--refresh-interval",
            "45",
        ]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                args_call, kwargs = AE.call_args
                self.assertEqual(args_call[0], ["cli-term"])
                self.assertEqual(kwargs.get("refresh_interval"), 45)
                self.assertEqual(kwargs.get("marketplaces"), ["ebay"])
                self.assertEqual(kwargs.get("deal_threshold"), 0.4)


if __name__ == "__main__":
    unittest.main()
