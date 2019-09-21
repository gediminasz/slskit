hello:
  cmd.run:
    - name: echo "Hello, I'm {{ pillar.name }}!"

system_timezone:
  timezone.system:
    - name: UTC
