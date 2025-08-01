# ArbitrageEngine - Pseudocode Outline
#
# This module sketches out the design of a personal AI tool that scans
# various public marketplaces looking for arbitrage opportunities.
# It illustrates how the engine could be organized in Python.

import asyncio
import re
from urllib.parse import quote_plus

import aiohttp
from bs4 import BeautifulSoup


class ArbitrageEngine:
    """High level pseudocode for the arbitrage detection engine."""

    def __init__(
        self,
        search_terms,
        refresh_interval=60,
        alert_callback=None,
        marketplaces=None,
        deal_threshold=0.5,
    ):
        """Create a new engine instance.

        Parameters
        ----------
        search_terms : list[str]
            Keywords to search for on each marketplace.
        refresh_interval : int, optional
            How often to poll the marketplaces, by default ``60``.
        alert_callback : callable | None, optional
            Optional callback invoked when a deal is found.
        marketplaces : Iterable[str] | None, optional
            Restrict queries to these marketplaces. If ``None`` all
            known marketplaces will be queried.
        """

        # Store search settings supplied by the user
        self.search_terms = search_terms  # e.g. categories or keywords
        self.refresh_interval = refresh_interval  # how often to scan markets
        self.alert_callback = alert_callback  # function to run on a detected deal
        self.deal_threshold = deal_threshold  # percentage of value to trigger deal alert

        default_markets = [
            "facebook",
            "ebay",
            "craigslist",
            "aliexpress",
            "mercari",
        ]
        self.marketplaces = list(marketplaces) if marketplaces else default_markets

    # ------------------------------------------------------------------
    # Marketplace query helpers
    # ------------------------------------------------------------------
    def _build_query(self):
        """Return a URL encoded query string from the search terms."""
        return "+".join(quote_plus(term) for term in self.search_terms)

    async def _async_get(self, url: str, session: aiohttp.ClientSession) -> str:
        """Fetch the response body for ``url`` using ``session``.

        Parameters
        ----------
        url : str
            The URL to request.
        session : :class:`aiohttp.ClientSession`
            An active HTTP session used to perform the request.

        Returns
        -------
        str
            The text body of the response.
        """
        async with session.get(url, timeout=5) as resp:
            return await resp.text()

    async def query_facebook(self, session: aiohttp.ClientSession):
        query = self._build_query()
        url = f"https://www.facebook.com/marketplace/search?q={query}"
        try:
            html = await self._async_get(url, session)
        except aiohttp.ClientError:
            return []
        return self.parse_facebook(html, base_url="https://www.facebook.com")

    async def query_ebay(self, session: aiohttp.ClientSession):
        query = self._build_query()
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
        try:
            html = await self._async_get(url, session)
        except aiohttp.ClientError:
            return []
        soup = BeautifulSoup(html, "html.parser")
        listings = []
        for item in soup.select("li.s-item"):
            title_el = item.select_one("h3.s-item__title")
            price_el = item.select_one("span.s-item__price")
            link_el = item.select_one("a.s-item__link")
            if not (title_el and link_el):
                continue
            title = title_el.get_text(strip=True)
            price = None
            if price_el:
                match = re.search(r"\$([0-9,.]+)", price_el.get_text())
                if match:
                    try:
                        price = float(match.group(1).replace(",", ""))
                    except ValueError:
                        price = None
            listings.append({"title": title, "price": price, "url": link_el["href"]})
        return listings

    async def query_craigslist(self, session: aiohttp.ClientSession):
        query = self._build_query()
        url = f"https://craigslist.org/search/sss?query={query}"
        try:
            html = await self._async_get(url, session)
        except aiohttp.ClientError:
            return []
        soup = BeautifulSoup(html, "html.parser")
        listings = []
        for item in soup.select("li.result-row"):
            title_el = item.select_one("a.result-title")
            price_el = item.select_one("span.result-price")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            price = None
            if price_el:
                match = re.search(r"\$([0-9,.]+)", price_el.get_text())
                if match:
                    try:
                        price = float(match.group(1).replace(",", ""))
                    except ValueError:
                        price = None
            url_item = title_el["href"]
            listings.append({"title": title, "price": price, "url": url_item})
        return listings

    async def query_aliexpress(self, session: aiohttp.ClientSession):
        query = self._build_query()
        url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
        try:
            html = await self._async_get(url, session)
        except aiohttp.ClientError:
            return []
        soup = BeautifulSoup(html, "html.parser")
        listings = []
        for item in soup.select("a[href][title][target]"):
            title = item.get("title")
            href = item.get("href")
            price_el = item.find_next("span", class_=lambda c: c and "price" in c)
            price = None
            if price_el:
                match = re.search(r"\$([0-9,.]+)", price_el.get_text())
                if match:
                    try:
                        price = float(match.group(1).replace(",", ""))
                    except ValueError:
                        price = None
            if title and href:
                listings.append({"title": title, "price": price, "url": href})
        return listings

    async def query_mercari(self, session: aiohttp.ClientSession):
        query = self._build_query()
        url = f"https://www.mercari.com/search/?keyword={query}"
        try:
            html = await self._async_get(url, session)
        except aiohttp.ClientError:
            return []
        soup = BeautifulSoup(html, "html.parser")
        listings = []
        for item in soup.select("li[data-testid='ItemCell']"):
            title_el = item.select_one("p[data-testid='ItemCell__name']")
            price_el = item.select_one("p[data-testid='ItemCell__price']")
            link_el = item.select_one("a")
            if not (title_el and link_el):
                continue
            title = title_el.get_text(strip=True)
            price = None
            if price_el:
                match = re.search(r"\$([0-9,.]+)", price_el.get_text())
                if match:
                    try:
                        price = float(match.group(1).replace(",", ""))
                    except ValueError:
                        price = None
            href = link_el.get("href")
            if href and not href.startswith("http"):
                href = f"https://www.mercari.com{href}"
            listings.append({"title": title, "price": price, "url": href})
        return listings

    # ------------------------------------------------------------------
    # HTML parsers
    # ------------------------------------------------------------------
    def parse_facebook(self, html: str, base_url: str) -> list[dict]:
        """Extract listings from a Facebook Marketplace search page."""
        soup = BeautifulSoup(html, "html.parser")
        listings = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/marketplace/item/" not in href:
                continue
            title = a.get("title")
            if not title:
                for text in a.stripped_strings:
                    if "$" not in text:
                        title = text
                        break
            price = None
            price_text = a.find(string=lambda t: t and "$" in t)
            if price_text:
                match = re.search(r"\$([0-9,.]+)", price_text)
                if match:
                    try:
                        price = float(match.group(1).replace(",", ""))
                    except ValueError:
                        price = None
            if not href.startswith("http"):
                href = f"{base_url}{href}"
            listings.append({"title": title, "price": price, "url": href})
        return listings

    async def fetch_listings(self):
        """Fetch listings from each marketplace concurrently."""
        tasks = []
        async with aiohttp.ClientSession() as session:
            for market in self.marketplaces:
                query_func = getattr(self, f"query_{market}", None)
                if query_func:
                    tasks.append(asyncio.create_task(query_func(session)))

            listings = []
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, Exception):
                        continue
                    for listing in result:
                        normalized = {
                            "title": listing.get("title"),
                            "price": listing.get("price"),
                            "url": listing.get("url"),
                        }
                        listings.append(normalized)
            return listings

    def evaluate_deals(self, listings):
        """Evaluate listings to find underpriced items."""
        # Iterate over listings and estimate each one's fair market value.
        # If a listing's asking price is lower than the configured threshold
        # of the predicted value, yield it as a potential deal.
        for listing in listings:
            predicted_price = self.predict_resale_value(listing)
            price = listing.get("price") if isinstance(listing, dict) else getattr(listing, "price", None)

            if price is None or predicted_price is None:
                continue

            if price < predicted_price * self.deal_threshold:
                yield listing, predicted_price

    def predict_resale_value(self, listing):
        """Return a naive estimate of the listing's resale value."""
        # This stub demonstrates where one could integrate an API call or a
        # machine learning model.  If the listing already contains a market
        # value field, prefer that.  Otherwise fall back to a simple heuristic.
        if isinstance(listing, dict):
            for key in ("market_value", "predicted_price", "estimated_price"):
                if key in listing:
                    return listing[key]
            price = listing.get("price")
        else:
            for key in ("market_value", "predicted_price", "estimated_price"):
                if hasattr(listing, key):
                    return getattr(listing, key)
            price = getattr(listing, "price", None)

        if price is None:
            return None

        # Simple heuristic: assume potential resale value is 150% of asking price
        return price * 1.5

    def alert(self, listing, predicted_price):
        """Notify the user about a potential arbitrage opportunity."""
        # Basic placeholder: print the deal. In a real application, this could
        # send an email, push notification, etc.
        if self.alert_callback:
            self.alert_callback(listing, predicted_price)
        else:
            print(f"Deal found: {listing} (est. value ${predicted_price})")

    async def run(self, iterations=None):
        """Continuously monitor marketplaces for deals.

        This coroutine repeatedly polls the configured marketplaces,
        evaluates any discovered listings and then waits for the
        configured refresh interval before the next scan.
        """
        runs = 0
        while True:
            listings = await self.fetch_listings()
            for listing, price in self.evaluate_deals(listings):
                self.alert(listing, price)
            runs += 1
            if iterations is not None and runs >= iterations:
                break
            await asyncio.sleep(self.refresh_interval)


def main() -> None:
    """Simple command line interface for :class:`ArbitrageEngine`."""
    import argparse

    parser = argparse.ArgumentParser(description="Run the Arbitrage Engine")
    parser.add_argument(
        "search_terms",
        nargs="+",
        help="One or more search terms to look for across marketplaces.",
    )
    parser.add_argument(
        "--refresh-interval",
        type=int,
        default=60,
        help="How often to scan the marketplaces in seconds.",
    )
    parser.add_argument(
        "--marketplaces",
        action="append",
        help=(
            "Limit scans to these marketplaces. Can be specified multiple "
            "times or as a comma separated list."
        ),
    )
    parser.add_argument(
        "--deal-threshold",
        type=float,
        default=0.5,
        help="Percentage of predicted value below which a listing is considered a deal.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of scan iterations to run before exiting.",
    )
    args = parser.parse_args()

    marketplaces = None
    if args.marketplaces:
        marketplaces = []
        for entry in args.marketplaces:
            marketplaces.extend([m for m in entry.split(",") if m])

    engine = ArbitrageEngine(
        args.search_terms,
        refresh_interval=args.refresh_interval,
        marketplaces=marketplaces,
        deal_threshold=args.deal_threshold,
    )
    asyncio.run(engine.run(iterations=args.iterations))


if __name__ == "__main__":
    main()

