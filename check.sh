#!/bin/sh

set -ex

black --check .
prospector
./tools/mypy.sh

slskit refresh
slskit snapshot check

pytest
