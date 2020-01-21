# slskit

![release](https://img.shields.io/github/release/gediminasz/slskit.svg)
![last commit](https://img.shields.io/github/last-commit/gediminasz/slskit.svg)
![build](https://img.shields.io/travis/gediminasz/slskit.svg)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: slskit [-h] [-c CONFIG] {highstate,pillars,refresh,snapshot} ...

slskit - tools for checking Salt state validity

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to slskit configuration file (default:
                        slskit.yaml or slskit.yml)

commands:
  {highstate,pillars,refresh,snapshot}
    highstate           render highstate for the specified minions
    pillars             render pillar items for the specified minions
    refresh             invoke saltutil.sync_all runner
    snapshot            create and check highstate snapshots
```
