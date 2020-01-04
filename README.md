# slskit

![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: slskit [-h] [-c CONFIG] {highstate,pillars} ...

slskit - tools for checking Salt state validity

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to slskit configuration file (default:
                        slskit.yaml or slskit.yml)

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
