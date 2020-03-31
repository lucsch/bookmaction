#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then

    # Install some custom requirements on macOS
    # e.g. brew install pyenv-virtualenv
    brew install python3
    pip install wxPython PyInstaller
else
    # Install some custom requirements on Linux
    pip install wxPython PyInstaller
fi