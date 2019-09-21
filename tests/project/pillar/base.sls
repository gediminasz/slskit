minion_id: {{ grains.id }}
grain_via_dict_access: {{ grains["id"] }}
secret: {{ salt['vault'].read_secret('foo/bar/baz', 'qux') }}
