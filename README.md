# Salinity

![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: salinity [-h] [-c CONFIG] {state.show_highstate,pillar.items} ...

Salinity - Salt testing toolkit.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to Salinity configuration file (default:
                        salinity.yaml or salinity.yml)

commands:
  {state.show_highstate,pillar.items}
    state.show_highstate
                        renders the states for the specified minions
    pillar.items        renders pillar items for the specified minions
```

## Projects for testing

- https://github.com/mitodl/salt-ops
- https://github.com/simpIeweblogic/saltstack
- https://github.com/Marmelatze/saltstack-mesos-test
- https://github.com/zulily/alkali
