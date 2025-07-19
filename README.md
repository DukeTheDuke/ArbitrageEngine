# ArbitrageEngine

A small demonstration project showing how one might build a tool to scan
online marketplaces for potential arbitrage opportunities.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

`aiohttp` is required to run the engine itself while `pytest` and
`pytest-asyncio` are used by the test suite.

## Usage

```bash
python ArbitrageEngine.py SEARCH_TERMS [SEARCH_TERMS ...] \
  [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]] \
  [--deal-threshold PERCENT] [--iterations N]
```

The optional `--marketplaces` flag limits scanning to the specified
sites. It can be provided multiple times or as a comma separated list.
By default the engine queries `facebook`, `ebay`, `craigslist`,
`aliexpress` and `mercari`.

Use `--deal-threshold` to adjust what percentage of the predicted value
is considered a bargain. The default is `0.5`.

Use `--iterations` to run the engine for a specific number of scan loops
before exiting. If omitted, the engine runs indefinitely.

```bash
python ArbitrageEngine.py phone --iterations 3 --marketplaces ebay,craigslist \
  --marketplaces mercari
```

## Running tests

After installing the dependencies you can run the test suite with
Python's built in `unittest` module:

```bash
python -m unittest
```
