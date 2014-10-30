#!/bin/bash

# Helper script to generate out RST files for API docs. It cleans out the old
# directory first to ensure no stale module RST files are hanging around before
# calling sphinx-apidoc.

if [ -d docs/source/api ]; then
    rm -rf docs/source/api
    mkdir docs/source/api
fi
sphinx-apidoc -T -o docs/source/api vyconf