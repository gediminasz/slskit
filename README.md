# Salinity

![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: salinity [-h] [-c CONFIG] {highstate,pillars} ...

Salinity - Salt testing toolkit.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to Salinity configuration file (default:
                        salinity.yaml or salinity.yml)

commands:
  {highstate,pillars}
    highstate           renders the states for the specified minions
    pillars             renders pillar items for the specified minions
```

## Projects for testing

- https://github.com/mitodl/salt-ops
- https://github.com/simpIeweblogic/saltstack
- https://github.com/Marmelatze/saltstack-mesos-test
- https://github.com/zulily/alkali
