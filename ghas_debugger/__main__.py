import os
import json
import logging
import argparse

from ghas_debugger.codeql.build import buildMetadata


CODEQL_ACTIONS_PATH = "/opt/hostedtoolcache/CodeQL/*/x64/codeql/codeql"


parser = argparse.ArgumentParser("GitHub Advance Security Debugger Action")
parser.add_argument(
    '--debug',
    action="store_true",
    default=bool(os.environ.get('DEBUG'))
)

parser.add_argument('-d', '--database', default=CODEQL_ACTIONS_PATH)
parser.add_argument('-b', '--binary', default=CODEQL_ACTIONS_PATH)

arguments = parser.parse_args()

# Logging
logging.basicConfig(
    level=logging.DEBUG if arguments.debug else logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


data = buildMetadata(arguments)

print(json.dumps(data, indent=2))
