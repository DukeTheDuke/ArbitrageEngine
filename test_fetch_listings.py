import pytest
from ArbitrageEngine import ArbitrageEngine

@pytest.mark.asyncio
async def test_fetch_listings_combines_results(monkeypatch):
    engine = ArbitrageEngine(search_terms=[])

    expected_fb = [{"title": "from facebook", "price": None, "url": None}]
    expected_ebay = [{"title": "from ebay", "price": None, "url": None}]
    expected_craigslist = [{"title": "from craigslist", "price": None, "url": None}]
    expected_aliexpress = [{"title": "from aliexpress", "price": None, "url": None}]
    expected_mercari = [{"title": "from mercari", "price": None, "url": None}]

    async def fake_fb(self, session):
        return expected_fb

    async def fake_ebay(self, session):
        return expected_ebay

    async def fake_craigslist(self, session):
        return expected_craigslist

    async def fake_aliexpress(self, session):
        return expected_aliexpress

    async def fake_mercari(self, session):
        return expected_mercari

    monkeypatch.setattr(ArbitrageEngine, "query_facebook", fake_fb)
    monkeypatch.setattr(ArbitrageEngine, "query_ebay", fake_ebay)
    monkeypatch.setattr(ArbitrageEngine, "query_craigslist", fake_craigslist)
    monkeypatch.setattr(ArbitrageEngine, "query_aliexpress", fake_aliexpress)
    monkeypatch.setattr(ArbitrageEngine, "query_mercari", fake_mercari)

    listings = await engine.fetch_listings()

    for listing in (
        expected_fb
        + expected_ebay
        + expected_craigslist
        + expected_aliexpress
        + expected_mercari
    ):
        assert listing in listings
