name: {{ grains["id"] }}
vault_secret: {{ salt["vault"].read_secret("secret/my/secret", "some-key") }}
