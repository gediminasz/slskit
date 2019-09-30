base:
  '*':
    - base
    - unknown

  'roles:via_pillar':
    - match: pillar
    - roles.via_pillar
