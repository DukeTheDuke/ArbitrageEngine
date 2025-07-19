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

    def test_custom_threshold_detection(self):
        engine = ArbitrageEngine(search_terms=[], deal_threshold=0.7)
        listings = [
            {"title": "under threshold", "price": 60, "market_value": 100},
            {"title": "above threshold", "price": 80, "market_value": 100},
        ]
        deals = list(engine.evaluate_deals(listings))
        self.assertEqual(len(deals), 1)
        self.assertEqual(deals[0][0]["title"], "under threshold")


class AlertCallbackTest(unittest.TestCase):
    def test_alert_callback_invoked(self):
        from unittest import mock

        callback = mock.Mock()
        engine = ArbitrageEngine(search_terms=[], alert_callback=callback)
        listings = [{"title": "steal", "price": 40, "market_value": 100}]

        for listing, predicted in engine.evaluate_deals(listings):
            engine.alert(listing, predicted)

        callback.assert_called_once_with(listings[0], 100)


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


class CLIThresholdTest(unittest.TestCase):
    def test_cli_parses_threshold(self):
        import sys
        from unittest import mock

        argv = [
            "prog",
            "item",
            "--deal-threshold",
            "0.25",
        ]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                _, kwargs = AE.call_args
                self.assertEqual(kwargs.get("deal_threshold"), 0.25)


class CLIRefreshIntervalTest(unittest.TestCase):
    def test_cli_parses_refresh_interval(self):
        import sys
        from unittest import mock

        argv = [
            "prog",
            "item",
            "--refresh-interval",
            "15",
        ]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                _, kwargs = AE.call_args
                self.assertEqual(kwargs.get("refresh_interval"), 15)


class CLIIterationsTest(unittest.TestCase):
    def test_cli_forwards_iterations(self):
        import sys
        from unittest import mock

        argv = [
            "prog",
            "item",
            "--iterations",
            "3",
        ]

        with mock.patch.object(sys, "argv", argv):
            with mock.patch("ArbitrageEngine.ArbitrageEngine") as AE:
                instance = AE.return_value
                from ArbitrageEngine import main

                main()
                AE.assert_called_once()
                instance.run.assert_called_once_with(iterations=3)


if __name__ == "__main__":
    unittest.main()
