import logging
import os


def getRepository():
    data = {}

    # Action support
    if os.environ.get("GITHUB_WORKFLOW"):
        logging.info("Running in Actions")
        data = getActionDetails()

    # TODO: Add more support

    # Non CI project / CLI
    else:
        data = {"name": os.path.basename(os.getcwd()), "workflow_type": "CLI"}

    return data


def getActionDetails():
    data = {"name": os.environ.get("GITHUB_REPOSITORY"), "workflow_type": "Actions"}
    return data
