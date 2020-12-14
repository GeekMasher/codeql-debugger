import os
import glob
import json
import logging
import argparse

from ghas_debugger.codeql.databases import getDatabases
from ghas_debugger.codeql.queries import Queries, getQueriesList


CODEQL_BINS = ["/usr/bin/codeql"]
# CodeQL Action
CODEQL_BINS.extend(glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/codeql"))

CODEQL_SEARCH_PATH = []
CODEQL_SEARCH_PATH.extend(
    glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/qlpacks/")
)

CODEQL_DATABASE = [""]
CODEQL_DATABASE.extend(glob.glob("/home/runner/work/_temp/codeql_databases/*"))


parser = argparse.ArgumentParser("GitHub Advance Security Debugger Action")
parser.add_argument(
    "--debug", action="store_true", default=bool(os.environ.get("DEBUG"))
)
parser.add_argument('--caching', action='store_true')

parser.add_argument("-d", "--databases", default="codeql-db")
parser.add_argument("-b", "--binary", default="codeql")
parser.add_argument("-dn", "--database-name")
parser.add_argument("-r", "--results", default=".codeql/results")
parser.add_argument("-s", "--search-path", default="queries")

arguments = parser.parse_args()

CODEQL_BINS.append(os.path.abspath(arguments.binary))
CODEQL_DATABASE.append(os.path.abspath(arguments.databases))
CODEQL_SEARCH_PATH.append(os.path.abspath(arguments.search_path))

# Logging
logging.basicConfig(
    level=logging.DEBUG if arguments.debug else logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logging.info("CodeQL Databases :: " + ",".join(CODEQL_DATABASE))
logging.info("CodeQL Binary :: " + ",".join(CODEQL_BINS))
logging.info("CodeQL Search Path :: " + ",".join(CODEQL_SEARCH_PATH))

# Gets a list of the CodeQL databases
databases = getDatabases(CODEQL_DATABASE, name=arguments.database_name)

codeql_queries = getQueriesList("./queries")

# Queries
queries = Queries(
    databases=databases,
    queries=codeql_queries,
    results="./results",
    codeql=os.path.abspath(arguments.binary),
    search_paths=CODEQL_SEARCH_PATH,
    caching=arguments.caching
)


METADATA = {
    "stasistics": {
        "loc": queries.findAndRunQuery("LinesOfCode"),
        # "comments": queries.findAndRunQuery("LinesOfComment")
    },
    "diagnostics": {
        "full":  queries.findAndRunQuery("Diagnostics"),
        "summary": queries.findAndRunQuery("DiagnosticsSummary"),
    }
}

# res = {
#     "java": {
#         "query_name": "LinesOfCode",
#         "path": "./results/LinesOfCode-java.csv"
#     }
# }
# METADATA = queries.getResults(res)


# data = buildMetadata(arguments)
print('='*32)
# with 
print(json.dumps(METADATA, indent=2))
