# Salinity

![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: salinity [-h] [--state-root STATE_ROOT] [--pillar-root PILLAR_ROOT]
                {state.show_highstate,pillar.items} ...

Salinity - Salt testing toolkit.

optional arguments:
  -h, --help            show this help message and exit
  --state-root STATE_ROOT
                        path to state root directory (default: salt)
  --pillar-root PILLAR_ROOT
                        path to pillar root directory (default: pillar)

commands:
  {state.show_highstate,pillar.items}
    state.show_highstate
                        renders the states for the specified minions
    pillar.items        renders pillar items for the specified minions
```

For example:

```
poetry run python -m salinity --state-root tests/project/salt --pillar-root tests/project/pillar state.show_highstate bob stuart
poetry run python -m salinity --state-root tests/project/salt --pillar-root tests/project/pillar pillar.items bob stuart
```

## Projects for testing

- https://github.com/mitodl/salt-ops
- https://github.com/simpIeweblogic/saltstack
- https://github.com/Marmelatze/saltstack-mesos-test
- https://github.com/zulily/alkali
