import sys

import yaml

from salinity.pillar.pillar_top import PillarTop

if __name__ == "__main__":
    pillar_top = PillarTop()
    result = {minion_id: pillar_top.for_minion(minion_id) for minion_id in sys.argv[1:]}
    print(yaml.dump(result, sort_keys=False))  # type: ignore
