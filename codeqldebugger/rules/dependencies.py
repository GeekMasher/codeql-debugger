import logging
from codeqldebugger.utils.issues import Issues


def projectLombokCheck(rule_id, metadata):
    # TODO: Logic
    Issues.addError(rule_id, "Project Lombok is present (java)")

    return
