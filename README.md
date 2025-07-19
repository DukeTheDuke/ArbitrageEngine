# ArbitrageEngine

A small demonstration project showing how one might build a tool to scan
online marketplaces for potential arbitrage opportunities.

## Usage

```bash
python ArbitrageEngine.py SEARCH_TERMS [SEARCH_TERMS ...] [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]]
python ArbitrageEngine.py --config PATH [--refresh-interval SECONDS] [--marketplaces SITE[,SITE...]] SEARCH_TERMS
```

The optional `--marketplaces` flag limits scanning to the specified
sites. It can be provided multiple times or as a comma separated list.

```
python ArbitrageEngine.py phone --marketplaces ebay,craigslist --marketplaces facebook
```

### Configuration file

Use the `--config` option to load default options from a JSON or YAML file. CLI
arguments override values in the configuration:

```bash
python ArbitrageEngine.py --config sample_config.yaml
```

The repository includes `sample_config.yaml` demonstrating the available
options.
