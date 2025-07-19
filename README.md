# ArbitrageEngine

A small demonstration project showing how one might build a tool to scan
online marketplaces for potential arbitrage opportunities.

## Usage

```bash
python ArbitrageEngine.py SEARCH_TERMS [SEARCH_TERMS ...] [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]] [--log-level LEVEL]
```

The optional `--marketplaces` flag limits scanning to the specified
sites. It can be provided multiple times or as a comma separated list.

`--log-level` controls the verbosity of output. Valid values are the standard
Python logging levels such as `INFO` or `DEBUG`.

```
python ArbitrageEngine.py phone --marketplaces ebay,craigslist --marketplaces facebook
```
