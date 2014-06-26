#!/bin/sh

which trang 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "trang binary not found"
    echo "Install trang (http://www.thaiopensource.com/relaxng/trang.html) or make sure it is in your PATH"
    exit 1
fi

source=$1
destination=$2
if [ ! -f $source ]; then
    echo "Source file $source does not exist"
    exit 1
fi

if [ -z $destination ]; then
    echo "Please specify destination file"
    exit 1
fi

echo "Writing RelaxNG into $destination"
trang -Irnc -Orng $source $destination
