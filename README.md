# ArbitrageEngine

A small demonstration project showing how one might build a tool to scan
online marketplaces for potential arbitrage opportunities.

## Installation

Install the required dependencies with pip:

```bash
pip install aiohttp
```

## Usage

```bash
python ArbitrageEngine.py SEARCH_TERMS [SEARCH_TERMS ...] [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]]
```

The optional `--marketplaces` flag limits scanning to the specified
sites. It can be provided multiple times or as a comma separated list.

```
python ArbitrageEngine.py phone --marketplaces ebay,craigslist --marketplaces facebook
```
