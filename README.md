# slskit

![release](https://img.shields.io/github/release/gediminasz/slskit.svg)
![last commit](https://img.shields.io/github/last-commit/gediminasz/slskit.svg)
![build](https://github.com/gediminasz/slskit/workflows/CI/badge.svg?branch=master)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
usage: slskit [-h] [-V] [-c CONFIG]
              [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET,QUIET,PROFILE,TRACE,GARBAGE}]
              {highstate,sls,pillars,template,refresh,snapshot} ...

slskit - tools for checking Salt state validity

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to slskit configuration file (default:
                        slskit.yaml or slskit.yml)
  -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET,QUIET,PROFILE,TRACE,GARBAGE}, --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET,QUIET,PROFILE,TRACE,GARBAGE}

commands:
  {highstate,sls,pillars,template,refresh,snapshot}
    highstate           render highstate for specified minions
    sls                 render a given sls for specified minions
    pillars             render pillar items for specified minions
    template            render a file template for specified minions
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

## Workaround for exception raised when processing __virtual__ function

When seeing errors like these:

```
ERROR:salt.loader:Exception raised when processing __virtual__ function for salt.loaded.int.module.freebsdkmod. Module will not be loaded: 'kernel'
WARNING:salt.loader:salt.loaded.int.module.freebsdkmod.__virtual__() is wrongly returning `None`. It should either return `True`, `False` or a new name. If you're the developer of the module 'freebsdkmod', please fix this.
```

You may need to add a corresponding grain to `slskit.yaml` file, e.g.:

```yaml
# slskit.yaml

slskit:
  roster:
    foo:
      grains:
        kernel: Linux
```

You can find values for grains by inspecting `grains.items` on your real minions.

## How to keep your grains DRY

Use `default_grains` option to avoid duplicating the same grains over all minions:

```yaml
# slskit.yaml

slskit:
  roster:
    foo:
    bar:
    baz:
  default_grains:
    os: Ubuntu
```

For more advanced cases use YAML anchors:

```yaml
# slskit.yaml

_grains:
  ubuntu: &ubuntu
    os: Ubuntu
  fedora: &fedora
    os: Fedora

slskit:
  roster:
    u1:
      grains:
        <<: *ubuntu
    u2:
      grains:
        <<: *ubuntu
    f1:
      grains:
        <<: *fedora
    f2:
      grains:
        <<: *fedora
```
