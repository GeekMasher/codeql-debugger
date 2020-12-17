# CodeQL Debugger

CodeQL Debugging Action

## CI

### Actions

```yml
    # ...
    # Upload CodeQL Databases
    - uses: actions/upload-artifact@v2
      with:
        name: codeql-databases-${{ matrix.language }}
        path: /home/runner/work/_temp/codeql_databases/

  debugger:
    name: CodeQL Debugger
    runs-on: ubuntu-latest
    needs: [analyze]
    
    steps:
      # Download CodeQL Databases
      - uses: actions/download-artifact@v2
      # Lazy loading and install
      - name: CodeQL Deubgger Lazy Load
        run: |
          curl -o- https://raw.githubusercontent.com/GeekMasher/codeql-debugger/main/scripts/install.sh | bash


```

## Manual

### CLI

```bash

```

### Docker Image

```bash
# Building
docker build -t geekmasher/codeql-debugger .

# Running the container
docker run -v  geekmasher/codeql-debugger
```
