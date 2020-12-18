import logging
from codeqldebugger.utils.issues import Issues


def kotlinDetected(rule_id, metadata):
    Issues.addWarning(rule_id, "Kotlin source code detected in the repository")
    return


def jspCheck(rule_id, metadata):
    # TODO: Logic
    Issues.addWarning(
        rule_id, "JSP file detected but not supported by CodeQL (java/jsp)"
    )

    return
