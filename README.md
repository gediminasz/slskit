# Salinity

```
usage: salinity [-h] [--state-root STATE_ROOT] [--state-top STATE_TOP]
                [--pillar-root PILLAR_ROOT] [--pillar-top PILLAR_TOP]
                {state.show,pillar.top,pillar.items} ...

Salinity - Salt testing toolkit.

optional arguments:
  -h, --help            show this help message and exit
  --state-root STATE_ROOT
                        path to state root directory (default: salt)
  --state-top STATE_TOP
                        state top file name (default: top.sls)
  --pillar-root PILLAR_ROOT
                        path to pillar root directory (default: pillar)
  --pillar-top PILLAR_TOP
                        pillar top file name (default: top.sls)

commands:
  {state.show,pillar.top,pillar.items}
    state.show          renders the states for the specified minions
    pillar.top          renders the pillar top file
    pillar.items        renders pillar items for the specified minions
```

## Projects for testing

- https://github.com/mitodl/salt-ops
- https://github.com/simpIeweblogic/saltstack
- https://github.com/Marmelatze/saltstack-mesos-test
- https://github.com/zulily/alkali
