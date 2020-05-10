# slskit

![release](https://img.shields.io/github/release/gediminasz/slskit.svg)
![last commit](https://img.shields.io/github/last-commit/gediminasz/slskit.svg)
![build](https://github.com/gediminasz/slskit/workflows/CI/badge.svg?branch=master)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: slskit [-h] [-c CONFIG] {highstate,sls,pillars,refresh,snapshot} ...

slskit - tools for checking Salt state validity

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to slskit configuration file (default:
                        slskit.yaml or slskit.yml)

commands:
  {highstate,sls,pillars,refresh,snapshot}
    highstate           render highstate for specified minions
    sls                 render a given sls for specified minions
    pillars             render pillar items for specified minions
    refresh             invoke saltutil.sync_all runner
    snapshot            create and check highstate snapshots
```

---

## Workaround for libcrypto.dylib failing to load on macOS

If `slskit` fails with `zsh: abort` or `Abort trap: 6`, inspect the error by running the command with `PYTHONDEVMODE=1`. If the issue is with `_load_libcrypto` call in `rsax931.py`, edit `salt/utils/rsax931.py` line 38:

```diff
-lib = find_library('crypto')
+lib = "/usr/local/opt/openssl@1.1/lib/libcrypto.dylib"
```

More info:

- https://github.com/saltstack/salt/issues/55084
- https://github.com/Homebrew/homebrew-core/pull/45895/files#diff-5bdebf3b9146d50b15f9a0dc7e7def27R131-R133
