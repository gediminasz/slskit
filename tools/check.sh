#!/bin/sh

set -ex

black --check .
prospector
mypy --strict --allow-untyped-decorators

slskit refresh
slskit snapshot check

pytest
