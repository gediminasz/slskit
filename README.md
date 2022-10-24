# slskit

![release](https://img.shields.io/github/release/gediminasz/slskit.svg)
![python](https://img.shields.io/pypi/pyversions/slskit)
![build](https://github.com/gediminasz/slskit/workflows/CI/badge.svg?branch=master)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)

```
Usage: slskit [OPTIONS] COMMAND [ARGS]...

Options:
  --version                       Show the version and exit.
  -c, --config TEXT               path to slskit configuration file (default:
                                  slskit.yaml or slskit.yml)

  -l, --log-level [CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET|QUIET|PROFILE|TRACE|GARBAGE]
  --help                          Show this message and exit.

Commands:
  highstate  render highstate for specified minions
  pillars    render pillar items for specified minions
  refresh    invoke saltutil.sync_all runner
  sls        render a given sls for specified minions
  template   render a file template for specified minions
```

- Supported Python versions: 3.8, 3.9, 3.10
- Supported Salt versions: 3004, 3005

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

## How to reduce output verbosity

Use Salt's [`output` configuration option](https://docs.saltstack.com/en/latest/ref/configuration/master.html#output), e.g.:

```yaml
# slskit.yaml

salt:
  output: yaml

slskit:
  ...
```

---


## External links

- https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-version-support-lifecycle.html
- https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-python-version-support.html
