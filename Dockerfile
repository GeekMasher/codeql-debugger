FROM python:alpine

VOLUME [ "/opt/hostedtoolcache/", "/home/runner/work/_temp/codeql_databases" ]

ENV CODEQL_DIST=.codeql/bin/

WORKDIR /codeql-debugger

RUN apk update && \
    apk add --update py3-setuptools && \
    pip install pipenv

COPY . .

RUN pipenv install --system

WORKDIR /workspace

ENTRYPOINT [ "python3", "/codeql-debugger/codeqldebugger" ]
