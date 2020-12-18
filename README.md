# CodeQL Debugger

CodeQL Debugging Action

## Actions

```yaml
# Post-Analysis stages
# ...
# Lazy loading and install
- name: CodeQL Debugger
  run: |
    curl -o- https://raw.githubusercontent.com/GeekMasher/codeql-debugger/main/scripts/install.sh | bash
# Upload Results to Artifacts
- name: Publish CodeQL Debugger Result
  uses: actions/upload-artifact@v2
  with:
    name: codeql-debugger
    path: .codeql/results

```

### Actions: Matrix Build

Due to the way matrix builds work you will need to make sure before running the debugger all the CodeQL Databases are finalized.

```yaml
  analyze:
    # ...
    - name: Upload CodeQL Databases
      uses: actions/upload-artifact@v2
      with:
        name: codeql-databases-${{ matrix.language }}
        path: /home/runner/work/_temp/codeql_databases/

  # New Job that needs the analyze job to have completed
  debugger:
    name: CodeQL Debugger
    runs-on: ubuntu-latest
    needs: [analyze]
    
    steps:
      # Download CodeQL Databases
      - name: Download CodeQL Matrix build Artifacts
        uses: actions/download-artifact@v2
        with:
          path: .codeql/db
      # Lazy loading and install
      - name: CodeQL Deubgger
        run: |
          curl -o- https://raw.githubusercontent.com/GeekMasher/codeql-debugger/main/scripts/install.sh | bash
      # Upload Results to Artifacts
      - name: Publish CodeQL Debugger Result
        uses: actions/upload-artifact@v2
        with:
          name: codeql-debugger
          path: .codeql/results

```

### Extra Debugging

```yaml

  # Lazy loading and install
  - name: CodeQL Deubgger Lazy Load
    # Optional: If the debugger failed, it doesn't break the build
    continue-on-error: true
    # Optional: Enable debugging and additional output
    env:
      DEBUG: true
    run: |
      curl -o- https://raw.githubusercontent.com/GeekMasher/codeql-debugger/main/scripts/install.sh | bash

```

## Contributions
