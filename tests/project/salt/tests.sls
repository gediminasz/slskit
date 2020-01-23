test.common.pillar_access:
  test.show_notification:
    - text: "My name is {{ pillar.name }}!"

test.common.grain_access.id:
  test.show_notification:
    - text: "My id is {{ grains.id }}"

test.common.grain_access.custom:
  test.show_notification:
    - text: "My os is {{ grains.os }}"

test.vault.secret:
  test.show_notification:
    - text: "This is top secret: {{ pillar.vault.secret }}"
