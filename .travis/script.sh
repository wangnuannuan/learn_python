#!/bin/sh

die() {
    echo " *** ERROR: " $*
    exit 1
}

#set -x

[ "$TRAVIS_OS_NAME" != "linux" ] || {
    echo "$TRAVIS_PULL_REQUEST"
    git checkout -- . || die
    cd .travis || die
    python comment.py || die
    COMMENT="test send comments in bash script"
    bash -c "$COMMENTS"
}
