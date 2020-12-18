import logging
from codeqldebugger.utils.issues import Issues


def sources(id, metadata):
    for lang, data in metadata.get("analysis", {}).get("sources", {}).items():
        value = data.get("results", [{}])[0].get("col0", 0)

        # TODO: Low source count?
        if value == 0:
            Issues.addError(id, "No Sources Detected (" + lang + ")")

    return


def databaseSinks(id, metadata):

    for lang, data in metadata.get("analysis", {}).get("sinks_db", {}).items():
        value = data.get("results", [{}])[0].get("col0", 0)

        # Ignore JavaScript sinks (could be client code)
        if value == 0 and lang != "javascript":
            Issues.addWarning(id, "No SQL Sinks present (" + lang + ")")

    return


def xssSinks(id, metadata):

    for lang, data in metadata.get("analysis", {}).get("sinks_xss", {}).items():
        value = data.get("results", [{}])[0].get("col0", 0)

        # Ignore JavaScript sinks (could be client code)
        if value == 0:
            Issues.addWarning(id, "No XSS Sinks present (" + lang + ")")

    return
