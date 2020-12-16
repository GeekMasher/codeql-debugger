#!/bin/sh

# Prep
apt-get install -y git python3 python3-pip

# Clone latest
mkdir -p .codeql
git clone --depth=1 https://github.com/GeekMasher/codeql-debugger.git .codeql/debugger

# Install deps
python3 -m pip install --user pipenv
./.local/bin/pipenv install --system

# Run debugger
python3 .codeql/debugger/codeqldebugger
