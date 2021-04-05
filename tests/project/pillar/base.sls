minion_name: {{ grains["id"] }}

vault:
  secret: {{ salt["vault"].read_secret("secret/my/secret", "some-key") }}
