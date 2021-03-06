# Changelog

## 2020.9.0

- Changed `refresh` command to run `fileserver.update` before `saltutil.sync_all`.
- Fixed `highstate` command not showing any errors when pillar rendering fails.

## 2020.6.0

- Added `template` command which can be used to render file templates.
- Added `--log-level` parameter.

## 2020.5.1

- Added `slskit.default_grains` setting for specifying grains to be applied to all minions in roster.

## 2020.5.0

- Added `sls` command which can render a specific state (analogous to `state.show_sls`).
- Added `skip_fileserver_update` setting (enabled by default) to speed up highstate rendering for a large number of minions. The setting can be disabled in `slskit.yaml` config:

```yaml
slskit:
  skip_fileserver_update: false
```

## 2020.2.0

- Added `snapshot create` and `snapshot check` commands.

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
