#!/bin/sh
#
#    runtests.sh: runs tests
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA

if [ "$NOSETESTS" == "" ]; then
    NOSETESTS=nosetests
fi
echo "Using $NOSETESTS for nosetests binary"

which $NOSETESTS 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "nosetests binary not found"
    echo "Install nose (https://pypi.python.org/pypi/nose/‎) or make sure it is in your PATH"
    exit 1
fi

if $(scripts/checkmodule.py coverage); then
    COVERAGE_OPTIONS="--with-coverage --cover-branches"
else
    echo "Warning: install python coverage module (http://nedbatchelder.com/code/coverage/) to enable coverage report"
    COVERAGE_OPTIONS=""
fi

PYTHONPATH=libraries:tests/unit $NOSETESTS $COVERAGE_OPTIONS --verbosity=2 -w tests/unit/

PYTHONPATH=libraries:tests/integration \
VYCONF_DATA_DIR=$PWD/data/ \
VYCONF_TEST_DATA_DIR=$PWD/tests/integration/data \
$NOSETESTS --verbosity=2 -w tests/integration/
