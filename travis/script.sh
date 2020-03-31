#!/bin/bash

python install/createversion.py ../code/version.py
cd install

if [ $TRAVIS_OS_NAME = 'osx' ]; then
    # run some scripts on macOS
    # e.g. brew install pyenv-virtualenv
    python createapp.py OSX
    cd ..
    rm bin/dist/bookmaction
    python createdmg.py bookmaction bin/dist
else
    # run some scripts on Linux
    python createapp.py Linux
fi