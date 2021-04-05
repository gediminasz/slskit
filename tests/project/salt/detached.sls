test.detached.basic:
  test.show_notification:
    - text: "This sls is not mentioned in the top file and so it is not part of highstate."

test.detached.pillar_access:
  test.show_notification:
    - text: "My name is {{ pillar.minion_name }}"
