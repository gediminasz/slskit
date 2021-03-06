#!/bin/sh

set -ex

black --check .
mypy --strict --allow-untyped-decorators

slskit refresh
slskit snapshot check

pytest
