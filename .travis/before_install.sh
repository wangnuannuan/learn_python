#!/bin/sh

die() {
    echo " *** ERROR: " $*
    exit 1
}

#set -x


[ "$TRAVIS_OS_NAME" != "linux" ] || {

    pip install --upgrade pip || die "Failed to upgrade pip"
    pip install requests || die "Failed to install requests"

}
