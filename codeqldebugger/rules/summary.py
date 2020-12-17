import logging
from codeqldebugger.utils.issues import Issues


def databaseSinks(id, metadata):

    for lang, data in metadata.get("analysis", {}).get("sinks_db", {}).items():
        value = data.get("results", [{}])[0].get("col0", 0)

        # Ignore JavaScript sinks (could be client code)
        if value == 0 and lang != "javascript":
            Issues.addWarning(id, "No SQL Sinks present (" + lang + ")")

    return
