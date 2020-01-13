# slskit

![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: slskit [-h] [-c CONFIG] {highstate,pillars,refresh} ...

slskit - tools for checking Salt state validity

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to slskit configuration file (default:
                        slskit.yaml or slskit.yml)

commands:
  {highstate,pillars,refresh}
    highstate           renders the states for the specified minions
    pillars             renders pillar items for the specified minions
    refresh             invokes saltutil.sync_all runner
```
