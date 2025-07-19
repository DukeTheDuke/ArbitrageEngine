import unittest
from ArbitrageEngine import ArbitrageEngine

class FacebookParserTest(unittest.TestCase):
    def test_parse_facebook_basic(self):
        html = (
            '<div><a href="/marketplace/item/123">'
            '<div class="title">Old Phone</div>'
            '<span>$50</span>'
            '</a></div>'
        )
        engine = ArbitrageEngine(search_terms=[])
        listings = engine.parse_facebook(html, base_url="https://www.facebook.com")
        self.assertEqual(len(listings), 1)
        listing = listings[0]
        self.assertEqual(listing["title"], "Old Phone")
        self.assertEqual(listing["price"], 50.0)
        self.assertEqual(listing["url"], "https://www.facebook.com/marketplace/item/123")

if __name__ == "__main__":
    unittest.main()
