#!/bin/sh

set -ex

black --check .
pylint slskit tests
mypy --strict --allow-untyped-decorators

slskit refresh
slskit highstate | diff highstate.snap -

pytest
