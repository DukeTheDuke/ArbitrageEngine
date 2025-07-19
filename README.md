# ArbitrageEngine

ArbitrageEngine is a simple proof-of-concept script that demonstrates how one might scan multiple marketplaces for potential arbitrage opportunities.

## Installation

Use Python 3. Install the single dependency using:

```bash
pip install -r requirements.txt
```

## Usage

Run the engine from the command line, providing one or more search terms. Optional flags allow you to adjust the refresh interval and set the marketplaces to query.

```bash
python ArbitrageEngine.py <search terms> [--refresh-interval SECONDS] [--marketplaces list]
```

* `--refresh-interval` sets how frequently the marketplaces are scanned (defaults to `60`).
* `--marketplaces` is a comma-separated list of marketplaces to scan (defaults to `facebook,ebay,craigslist,aliexpress`).

Example:

```bash
python ArbitrageEngine.py laptop phone --refresh-interval 120 --marketplaces facebook,ebay
```

## Running Tests

Execute the test suite with:

```bash
python -m unittest test.py
```
