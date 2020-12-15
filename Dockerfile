FROM python:alpine

WORKDIR /codeql-debugger

RUN apk update && \
    apk add --update py3-setuptools && \
    pip install pipenv

COPY . .

RUN pipenv install --system

WORKDIR /workspace

ENTRYPOINT [ "python3", "/codeql-debugger/codeqldebugger" ]
