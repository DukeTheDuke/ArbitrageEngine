# ArbitrageEngine

A small demonstration project showing how one might build a tool to scan
online marketplaces for potential arbitrage opportunities.

## Usage

```bash
python ArbitrageEngine.py SEARCH_TERMS [SEARCH_TERMS ...] [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]] [--deal-threshold PERCENT]
```

The optional `--marketplaces` flag limits scanning to the specified
sites. It can be provided multiple times or as a comma separated list.

Use `--deal-threshold` to adjust what percentage of the predicted value
is considered a bargain. The default is `0.5`.

```
python ArbitrageEngine.py phone --marketplaces ebay,craigslist --marketplaces facebook
```
