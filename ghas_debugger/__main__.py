import os
import json
import logging
import argparse

from ghas_debugger.codeql.databases import getDatabases
from ghas_debugger.codeql.queries import Queries


CODEQL_ACTIONS_PATH = "/opt/hostedtoolcache/CodeQL/*/x64/codeql/codeql"


parser = argparse.ArgumentParser("GitHub Advance Security Debugger Action")
parser.add_argument(
    '--debug',
    action="store_true",
    default=bool(os.environ.get('DEBUG'))
)

parser.add_argument('-d', '--databases', default=CODEQL_ACTIONS_PATH)
parser.add_argument('-dn', '--database-name')
parser.add_argument('-b', '--binary', default=CODEQL_ACTIONS_PATH)

arguments = parser.parse_args()

# Logging
logging.basicConfig(
    level=logging.DEBUG if arguments.debug else logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logging.info("CodeQL Binary :: " + os.path.abspath(arguments.binary))


# Gets a list of the CodeQL databases
databases = getDatabases(
    os.path.abspath((arguments.databases)),
    name=arguments.database_name
)
# Queries
queries = Queries(
    databases=databases,
    codeql=os.path.abspath(arguments.binary),
)

# [print(loc) for loc in queries.getQueriesList()]
# exit()
loc = queries.findQuery('LinesOfCode')
queries.runQuery(loc[0], 'results/test.csv')
print(loc)


# data = buildMetadata(arguments)

# print(json.dumps(data, indent=2))
