import pytest
from ArbitrageEngine import ArbitrageEngine

@pytest.mark.parametrize(
    "terms,expected",
    [
        (["hello world"], "hello+world"),
        (["phone & charger"], "phone+%26+charger"),
        (["hello world", "foo/bar"], "hello+world+foo%2Fbar"),
    ],
)
def test_build_query_encoding(terms, expected):
    engine = ArbitrageEngine(search_terms=terms)
    assert engine._build_query() == expected
