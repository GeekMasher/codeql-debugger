import os
import glob
import json
import logging
import argparse

from ghas_debugger.codeql.databases import getDatabases
from ghas_debugger.codeql.queries import Queries, getQueriesList
from ghas_debugger.repository import getRepository
from ghas_debugger.ghas_render import render


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
parser.add_argument("--caching", action="store_true")

parser.add_argument("-d", "--databases", default=".codeql/db")
parser.add_argument("-b", "--binary", default="codeql")
parser.add_argument("-dn", "--database-name")
parser.add_argument("-r", "--results", default=".codeql/results")
parser.add_argument("-s", "--search-path", default="queries")
parser.add_argument("-o", "--output", default="results.json")

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

# Default: Result.json
result_outout = os.path.join(arguments.results, arguments.output)

# Gets a list of the CodeQL databases
databases = getDatabases(CODEQL_DATABASE, name=arguments.database_name)

codeql_queries = getQueriesList("./queries")

# Queries
queries = Queries(
    databases=databases,
    queries=codeql_queries,
    results=arguments.results,
    codeql=os.path.abspath(arguments.binary),
    search_paths=CODEQL_SEARCH_PATH,
    caching=arguments.caching,
)

# Create result dirs
if not os.path.exists(arguments.results):
    logging.debug("Creating results dir :: " + arguments.results)
    os.makedirs(arguments.results)

if not os.path.exists(queries.results_log):
    logging.debug("Creating results logs dir :: " + queries.results_log)
    os.makedirs(queries.results_log)

if not os.path.exists(queries.results_artifacts):
    logging.debug("Creating results artifacts dir :: " + queries.results_artifacts)
    os.makedirs(queries.results_artifacts)


if arguments.caching and os.path.exists(result_outout):
    # Load cached copy if enabled
    logging.info("Loading cached copy of the results")
    with open(result_outout, "r") as handle:
        METADATA = json.load(handle)

else:
    METADATA = {
        "repository": getRepository(),
        "statistics": {
            "loc": queries.findAndRunQuery("LinesOfCode"),
            "comments": queries.findAndRunQuery("LinesOfComment"),
            # "extensions": queries.findAndRunQuery("FileExtensions"),
        },
        "analysis": {"sources": {}, "sinks": {}, "sinks_db": {}, "sinks_external": {}},
        "diagnostics": {
            "full": queries.findAndRunQuery("Diagnostics"),
            "summary": queries.findAndRunQuery("DiagnosticsSummary"),
        },
    }


# data = buildMetadata(arguments)
if arguments.debug:
    print("=" * 32)
    print(json.dumps(METADATA, indent=2))
    print("=" * 32)

logging.info("Writing results output file :: " + result_outout)

with open(result_outout, "w") as handle:
    json.dump(METADATA, handle, indent=2)

logging.debug("Results written to storage")

render(METADATA, "result.html")
