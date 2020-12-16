import os
import csv
import json
import logging
import subprocess
from os.path import join, splitext


def repo_extensions(d):
    extensions = {}
    for root, dirs, files in os.walk(d):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            filepath = join(root, f)
            _, ext = splitext(filepath)
            ext = ext[1:]
            extensions[ext] = extensions.get(ext, 0) + 1
    return extensions


def compare_extensions(ondisk, indb):
    result = {}
    for ext in ondisk:
        result[ext] = (ondisk[ext], indb.get(ext, 0))

    result = list(result.items())
    result.sort(key=lambda i: i[1], reverse=True)
    return result


def getQueriesList(*roots, language=None):
    logging.debug("Loading queries")

    results = []

    for root in roots:
        logging.debug("Loading queries from path :: " + root)
        query_files = []

        for dp, dn, filenames in os.walk(root):
            for f in filenames:
                path = os.path.join(dp, f)
                if os.path.splitext(path)[1] == ".ql":
                    query_files.append(path)

        logging.debug("Number of Query File :: " + str(len(query_files)))

        for query in query_files:
            lang = os.path.split(query.replace(root, ""))[0]

            results.append(
                {
                    "name": os.path.splitext(os.path.basename(query))[0],
                    "path": os.path.abspath(query),
                    "language": lang.replace("/", ""),
                }
            )

    logging.info("Number of Queries loaded :: " + str(len(results)))

    return results


class Queries:
    def __init__(
        self,
        languages=[],
        results: str = None,
        queries: list = [],
        databases: list = None,
        codeql: str = None,
        search_path: list = [],
        caching: bool = False,
    ):
        self.queries = queries
        self.languages = languages
        self.codeql_exec = codeql
        self.databases = databases
        self.search_path = search_path

        self.data = {}

        self.results = results
        self.results_log = os.path.join(self.results, "logs")
        self.results_artifacts = os.path.join(self.results, "artifacts")

        self.caching = caching

    def findAndRunQuery(self, name, language=None):
        results = {}
        logging.info("Running query on CodeQL DB :: " + name)

        for database in self.databases:
            logging.debug("Loading database :: " + database.get("name"))
            queries = self.findQueries(name, database.get("language"))

            if len(queries) == 0:
                logging.warning("No queries to be run on CodeQL Database")

            for query in queries:
                logging.info("Selected Query :: {name} ({language})".format(**query))
                result = self.runQuery(query, database, self.results)

                results[database.get("language")] = result

        # print(json.dumps(results, indent=2))

        return self.getResults(results)

    def findQueries(self, name, language=None):
        results = []

        for query in self.queries:
            if query.get("name") == name:
                results.append(query)

        return results

    def runQuery(self, query, database, output):
        """

        output: Dir of
        """
        if self.codeql_exec is None:
            raise Exception("CodeQL binary isn't loaded")

        result = {}

        file_format = "{query_name}-{language}.{format}"
        # Local env
        env = os.environ.copy()
        env["CODEQL_DIST"] = os.path.join(
            os.getcwd(), os.path.dirname(self.codeql_exec)
        )

        file_output_bqrs = os.path.join(
            self.results_artifacts,
            file_format.format(
                query_name=query.get("name"),
                language=database.get("language"),
                format="bqrs",
            ),
        )

        if self.caching and os.path.exists(file_output_bqrs):
            logging.info("Using cached copy of the query :: " + query.get("name"))
        else:
            # Caching disabled or doesn't exist

            logging.debug("CodeQL query run Output :: " + file_output_bqrs)

            command = [
                self.codeql_exec,
                "query",
                "run",
                "--search-path",
                self.search_path,
                "-d",
                database.get("path"),
                "-o",
                file_output_bqrs,
                query.get("path"),
            ]

            logging.debug("CodeQL Command :: " + str(command))

            file_output_bqrs_logs = os.path.join(
                self.results_log,
                file_format.format(
                    query_name=query.get("name"),
                    language=database.get("language"),
                    format="log",
                ),
            )

            logging.debug("Setting env to null")
            with open(file_output_bqrs_logs, "w") as handle:
                subprocess.run(command, stdout=handle, stderr=handle, env={})

            if not os.path.exists(file_output_bqrs):
                logging.error("BQRS file does not exist")
                with open(file_output_bqrs_logs, "r") as handle:
                    logging.error(handle.read())
                raise Exception("BQRS file does not exist")

        # BQRS to format
        file_output_csv = os.path.join(
            self.results_artifacts,
            file_format.format(
                query_name=query.get("name"),
                language=database.get("language"),
                format="csv",
            ),
        )

        command = [
            self.codeql_exec,
            "bqrs",
            "decode",
            "--format=csv",
            "-o",
            file_output_csv,
            file_output_bqrs,
        ]

        logging.debug("CodeQL Command :: " + str(command))

        file_output_csv_logs = os.path.join(
            self.results_log,
            file_format.format(
                query_name=query.get("name"),
                language=database.get("language"),
                format="log",
            ),
        )
        with open(file_output_csv_logs, "w") as handle:
            subprocess.run(command, stdout=handle, stderr=handle, env={})

        result = {
            "query_name": query.get("name"),
            "path": file_output_csv,
        }

        return result

    def getResults(self, results):
        # Processing Result files
        logging.info("Process result files")

        return_results = {}

        for language, result in results.items():

            logging.debug("Processing Result file :: " + result.get("path"))

            # Parse CSV to results
            with open(result.get("path"), "r") as handle_csv:
                csv_reader = csv.DictReader(handle_csv, delimiter=",", quotechar='"')

                result["results"] = []
                for row in csv_reader:
                    result["results"].append(row)

                return_results[language] = result

        return return_results
