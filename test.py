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


class AlertCsvTest(unittest.TestCase):
    def test_alert_appends_csv(self):
        import csv
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name

        try:
            engine = ArbitrageEngine(search_terms=[], csv_file=path)
            engine.alert({"title": "x"}, 1)
            with open(path, newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[-1], ["{'title': 'x'}", "1"])
        finally:
            os.remove(path)


class CLIOutputCsvTest(unittest.TestCase):
    def test_cli_parses_output_csv(self):
        import sys
        from unittest import mock

        argv = ["prog", "item", "--output-csv", "file.csv"]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                _, kwargs = AE.call_args
                self.assertEqual(kwargs.get("csv_file"), "file.csv")


if __name__ == "__main__":
    unittest.main()
