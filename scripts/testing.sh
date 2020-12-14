#!/bin/bash

pipenv run python -m ghas_debugger \
    --debug \
    -b ../codeql/bin/codeql-cli/codeql \
    -d ../codeql/databases/WebGoat
