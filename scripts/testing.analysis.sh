#!/bin/bash

../codeql/bin/codeql-cli/codeql database analyze \
    --additional-packs ./queries/java \
    --format csv \
    --output /Users/geekmasher/Documents/development/security-debugging/results/java-lines_of_code.csv \
    ../codeql/databases/WebGoat \
    /Users/geekmasher/Documents/development/security-debugging/queries/java/LinesOfCode.ql
