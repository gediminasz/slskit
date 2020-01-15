# Changelog

## 2020.1.3

- Changed `slskit.roster` namespace to allow null values in `slskit.yaml` config.
- Changed `highstate` and `pillars` commands to return exit code 1 in case of rendering errors.
- Changed `refresh` command to invoke `saltutil.sync_all` runner.
  - This enables one to define custom Salt extensions which can mock certain modules such as Vault.

## 2020.1.2

- Added `refresh` command which invokes Salt fileserver update.
  - Useful e.g. when using `gitfs`.

## 2020.1.1

- Renamed package to `slskit`.
- Improved package description on PyPI.

## 2020.1.0

- Added `highstate` command.
- Added `pillars` command.
