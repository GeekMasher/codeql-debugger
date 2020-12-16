import os
import sys
import glob
import json
import logging
import argparse

# TODO: better improve this
__HERE__ = os.path.dirname(os.path.realpath(__file__))
sys.path.append("/codeql-debugger")
# Root repo dir
sys.path.append(os.path.join(os.getcwd(), ".codeql", "debugger"))

from codeqldebugger.__version__ import *
from codeqldebugger.codeql.databases import getDatabases
from codeqldebugger.codeql.queries import (
    Queries,
    getQueriesList,
    repo_extensions,
    compare_extensions,
)
from codeqldebugger.repository import getRepository
from codeqldebugger.ghas_render import render


CODEQL_BINS = [".codeql/bin/codeql", "/usr/bin/codeql"]
# CodeQL Action
CODEQL_BINS.extend(glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/codeql"))

CODEQL_SEARCH_PATHS = [".codeql/bin/codeql/qlpacks"]
CODEQL_SEARCH_PATHS.extend(
    glob.glob("/opt/hostedtoolcache/CodeQL/*/x64/codeql/qlpacks/")
)

CODEQL_DATABASE = [
    ".codeql/db",
    "/home/runner/work/_temp/codeql_databases/",
]


parser = argparse.ArgumentParser("GitHub Advance Security Debugger Action")
parser.add_argument(
    "--debug", action="store_true", default=bool(os.environ.get("DEBUG"))
)
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--caching", action="store_true")

parser.add_argument("-d", "--databases", default="")
parser.add_argument("-b", "--binary", default="codeql")
parser.add_argument("-dn", "--database-name")
parser.add_argument("-r", "--results", default=".codeql/results")
parser.add_argument("-s", "--search-path", default="queries")
parser.add_argument("-o", "--output", default="results.json")

arguments = parser.parse_args()

CODEQL_BINS.append(os.path.abspath(arguments.binary))
CODEQL_DATABASE.append(os.path.abspath(arguments.databases))
CODEQL_SEARCH_PATHS.append(os.path.abspath(arguments.search_path))

# Logging
logging.basicConfig(
    level=logging.DEBUG if arguments.debug else logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

logging.debug("CodeQL Databases Locations :: " + ",".join(CODEQL_DATABASE))
logging.debug("CodeQL Binary Locations :: " + ",".join(CODEQL_BINS))
logging.debug("CodeQL Search Locations :: " + ",".join(CODEQL_SEARCH_PATHS))

if not arguments.caching:
    logging.debug("Caching disabled")

# Default: Result.json
result_outout = os.path.join(arguments.results, arguments.output)

# Binaries
CODEQL_BIN = ""
for binary in CODEQL_BINS:
    binary = os.path.abspath(binary)
    if os.path.exists(binary):
        logging.info("Found CodeQL CLI :: " + binary)
        CODEQL_BIN = binary
        break

# Search QL Suites Paths
CODEQL_SEARCH_PATH = ""
for search_path in CODEQL_SEARCH_PATHS:
    search_path = os.path.abspath(search_path)
    if os.path.exists(search_path):
        logging.info("Found CodeQL QL Suite :: " + search_path)
        CODEQL_SEARCH_PATH = search_path
        break


# Gets a list of the CodeQL databases
databases = getDatabases(CODEQL_DATABASE, name=arguments.database_name)

codeql_queries = getQueriesList("./queries", "/codeql-debugger/queries")

if arguments.debug and arguments.verbose:
    for query in codeql_queries:
        logging.debug('<Query name="{name}" path="{path}"'.format(**query))

# Queries
queries = Queries(
    databases=databases,
    queries=codeql_queries,
    results=arguments.results,
    codeql=CODEQL_BIN,
    search_path=CODEQL_SEARCH_PATH,
    caching=arguments.caching,
)

# Create result dirs
logging.debug("Path - Results :: " + arguments.results)
os.makedirs(arguments.results, exist_ok=True)

logging.debug("Path - Log Files :: " + queries.results_log)
os.makedirs(queries.results_log, exist_ok=True)

logging.debug("Path - Results Artifacts :: " + queries.results_artifacts)
os.makedirs(queries.results_artifacts, exist_ok=True)


# Load cached copy if enabled
if arguments.caching and os.path.exists(result_outout):
    logging.info("Loading cached copy of the results")
    with open(result_outout, "r") as handle:
        METADATA = json.load(handle)

else:
    logging.debug("Building metadata object")

    METADATA = {
        "repository": getRepository(),
        "issues": {"errors": [], "warnings": []},
        "statistics": {
            "loc": queries.findAndRunQuery("LinesOfCode"),
            "comments": queries.findAndRunQuery("LinesOfComment"),
            # "extensions": queries.findAndRunQuery("FileExtensions"),
        },
        "analysis": {
            "sources": queries.findAndRunQuery("RemoteFlowSources"),
            "sinks": {},
            "sinks_db": queries.findAndRunQuery("SqlSinks"),
            "sinks_xxs": queries.findAndRunQuery("XssSinks"),
            "sinks_external": {},
        },
        "diagnostics": {
            "full": queries.findAndRunQuery("Diagnostics"),
            "summary": queries.findAndRunQuery("DiagnosticsSummary"),
        },
    }

    # METADATA["extensions"] = {}
    # feresults = (queries.findAndRunQuery("FileExtensions"),)
    # cwd = os.getcwd()
    # repo_exts = repo_extensions(cwd)
    # db_exts = {}
    # for lang in feresults:
    #     for row in list(lang.values())[0]["results"]:
    #         db_exts[row["extension"]] = int(row["frequency"])
    #     r = [
    #         {"extension": i[0], "in_checkout": i[1][0], "in_db": i[1][1]}
    #         for i in compare_extensions(repo_exts, db_exts)
    #     ]
    #     METADATA["extensions"][list(lang.keys())[0]] = r


if not databases:
    METADATA["issues"]["errors"].append(
        {"msg": "No Databases could be found on system.", "data": ""}
    )


# Print out the metadat / results.json
if arguments.debug and arguments.verbose:
    print("=" * 32)
    print(json.dumps(METADATA, indent=2))
    print("=" * 32)


logging.info("Writing results output file :: " + result_outout)

with open(result_outout, "w") as handle:
    json.dump(METADATA, handle, indent=2)

logging.info("Results written to storage")

render(METADATA, os.path.join(arguments.results, "result.html"))

logging.info("Finished CodeQL-Debugger")
