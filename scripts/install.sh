#!/bin/sh

# Prep
apt-get install -y git python3 python3-pip

# Clone latest
mkdir -p .codeql
git clone --depth=1 https://github.com/GeekMasher/codeql-debugger.git .codeql/debugger

# Install deps
python3 -m pip install jinja2

# Run debugger
PYTHONPATH="$PYTHONPATH:.codeql/debugger/"
python3 .codeql/debugger/codeqldebugger
