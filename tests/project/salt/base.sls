hello:
  cmd.run:
    - name: "Hello, my name is {{ pillar.name }} and I run {{ grains.os }}"
