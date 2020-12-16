#!/bin/sh

# Prep
apt-get install -y git python3 python3-pip

# Clone latest
mkdir -p .codeql
git clone --depth=1 https://github.com/GeekMasher/codeql-debugger.get .codeql/debugger

# Install deps
pip3 install pipenv
pipenv install --system

# Run debugger
python3 .codeql/debugger/codeqldebugger
