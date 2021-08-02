#!/usr/bin/env python3

import pantryscanner
import toml

CONFIG_FILE = "config.toml"
CONFIG_DEFAULT_FILE = "config-default.toml"

try:
    config = toml.load(CONFIG_FILE)
    config_default = toml.load(CONFIG_DEFAULT_FILE)
except (FileNotFoundError, toml.TomlDecodeError) as e:
    config = dict()
    config_default = toml.load(CONFIG_DEFAULT_FILE)

ps = pantryscanner.PantryScanner(config, config_default)
ps.start()
