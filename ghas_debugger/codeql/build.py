
import logging

from ghas_debugger.codeql.queries import Queries


def getLanguages():
    return ["java"]


def buildMetadata(arguments):
    logging.debug('Building metadata...')
    queries = Queries(
        languages=getLanguages(),
        database=arguments.database,
        codeql_bin=arguments.binary
    )

    queries_outputs = queries.runQueries()

    data = {"stasistics": {"loc": {"java": []}}}

    return queries_outputs
