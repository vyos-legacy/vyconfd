#!/bin/sh

which nosetests 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "nosetests binary not found"
    echo "Install nose (https://pypi.python.org/pypi/nose/‎) or make sure it is in your PATH"
    exit 1
fi

PYTHONPATH=libraries:tests/unit nosetests -w tests/unit/
