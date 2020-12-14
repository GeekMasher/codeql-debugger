import os
import glob
import json
import logging
import argparse

from ghas_debugger.codeql.databases import getDatabases
from ghas_debugger.codeql.queries import Queries


CODEQL_BINS = ["/usr/bin/codeql"]
# CodeQL Action
CODEQL_BINS.extend(glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/codeql"))

CODEQL_SEARCH_PATH = [""]
CODEQL_SEARCH_PATH.extend(
    glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/qlpacks/")
)

CODEQL_DATABASE = [""]
CODEQL_DATABASE.extend(glob.glob("/home/runner/work/_temp/codeql_databases/*"))


# print(CODEQL_BINS)
# exit()

parser = argparse.ArgumentParser("GitHub Advance Security Debugger Action")
parser.add_argument(
    "--debug", action="store_true", default=bool(os.environ.get("DEBUG"))
)

parser.add_argument("-d", "--databases", default="codeql-db")
parser.add_argument("-b", "--binary", default="codeql")
parser.add_argument("-dn", "--database-name")
parser.add_argument("-s", "--search-path", default="queries")

arguments = parser.parse_args()

CODEQL_BINS.append(arguments.binary)
CODEQL_DATABASE.append(arguments.database)
CODEQL_SEARCH_PATH.append(arguments.search_path)

# Logging
logging.basicConfig(
    level=logging.DEBUG if arguments.debug else logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logging.info("CodeQL Databases :: " + os.path.abspath(arguments.databases))
logging.info("CodeQL Binary :: " + os.path.abspath(arguments.binary))
logging.info("CodeQL Search Path :: " + arguments.search_path)

# Gets a list of the CodeQL databases
databases = getDatabases(
    os.path.abspath((arguments.databases)), name=arguments.database_name
)
# Queries
queries = Queries(
    databases=databases,
    results="./results",
    codeql=os.path.abspath(arguments.binary),
)

# [print(loc) for loc in queries.getQueriesList()]
# exit()
loc = queries.findQuery("LinesOfCode")
queries.runQuery(loc[0], "results/test.csv")
print(loc)


# data = buildMetadata(arguments)

# print(json.dumps(data, indent=2))
