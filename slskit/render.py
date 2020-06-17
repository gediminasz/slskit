import salt.loader
import salt.template

import slskit.pillar
from slskit.opts import Config


def render(config: Config):
    minion_id = "tester"
    grains = config.grains_for(minion_id)
    pillar = slskit.pillar.compile_pillar(config.opts, grains, minion_id).value

    opts = {**config.opts, "grains": grains, "pillar": pillar}
    functions = salt.loader.minion_mods(config.opts)
    renderers = salt.loader.render(opts, functions)

    output = salt.template.compile_template(
        "tests/project/salt/child.txt", renderers, "jinja", [], [], lol="LOL"
    )
    print(output.read())
