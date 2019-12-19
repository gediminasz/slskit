base:
  '*':
    - base

  'roles:via_pillar':
    - match: pillar
    - roles.via_pillar
