import pytest
from ArbitrageEngine import ArbitrageEngine


def fake_requester(market, terms):
    # return unique listing for each market
    return [
        {"market": market, "id": f"{market}-1", "price": 40, "estimated_value": 100},
        {"market": market, "id": f"{market}-2", "price": 70, "estimated_value": 100},
    ]


def test_fetch_listings():
    engine = ArbitrageEngine(["phone"], requester=fake_requester)
    listings = engine.fetch_listings()
    # Should combine results from all marketplaces
    expected_count = len(engine.marketplaces) * 2
    assert len(listings) == expected_count
    # Ensure listing structure preserved
    assert listings[0]["market"] in engine.marketplaces


def test_evaluate_deals():
    listings = [
        {"price": 40, "estimated_value": 100},
        {"price": 60, "estimated_value": 100},
        {"price": 10, "estimated_value": 50},
    ]
    engine = ArbitrageEngine(["phone"], requester=lambda m, t: [])
    deals = list(engine.evaluate_deals(listings))
    # Expect deals for items priced less than half their estimated value
    assert deals == [
        (listings[0], 100.0),
        (listings[2], 50.0),
    ]


def test_run(monkeypatch):
    collected = []

    def fake_alert(listing, price):
        collected.append((listing, price))

    sleep_calls = []
    engine = ArbitrageEngine(
        ["phone"],
        refresh_interval=0,
        alert_callback=fake_alert,
        requester=fake_requester,
        sleep_func=lambda s: sleep_calls.append(s),
    )

    # Run the loop only once by raising SystemExit after first sleep
    def stop_after_first_sleep(seconds):
        sleep_calls.append(seconds)
        raise SystemExit

    engine.sleep_func = stop_after_first_sleep
    with pytest.raises(SystemExit):
        engine.run()

    # Should have alerted deals from all marketplaces
    assert collected
    assert all(l[0]["price"] < l[1] * 0.5 for l in collected)

