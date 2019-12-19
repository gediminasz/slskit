hello:
  cmd.run:
    - name: echo "Hello, I am {{ pillar.name }}!"

system_timezone:
  timezone.system:
    - name: UTC
