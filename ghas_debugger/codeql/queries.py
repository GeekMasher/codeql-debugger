import os
import csv
import logging
import subprocess


def getQueriesList(root, language=None):
    query_files = []

    for dp, dn, filenames in os.walk(root):
        for f in filenames:
            path = os.path.join(dp, f)
            if os.path.splitext(path)[1] == ".ql":
                query_files.append(path)

    results = []
    for query in query_files:
        lang = os.path.split(query.replace(root, ""))[0]

        results.append(
            {
                "name": os.path.splitext(os.path.basename(query))[0],
                "path": os.path.abspath(query),
                "language": lang.replace("/", ""),
            }
        )

    return results


class Queries:
    def __init__(
        self,
        languages=[],
        results: str = None,
        queries: list = [],
        databases: list = None,
        codeql: str = None,
        search_paths: list = [],
        caching: bool = False,
    ):
        self.queries = queries
        self.languages = languages
        self.codeql_exec = codeql
        self.databases = databases
        self.search_paths = search_paths

        self.data = {}

        self.results = results
        self.results_log = os.path.join(self.results, "logs")
        self.results_artifacts = os.path.join(self.results, "artifacts")

        self.caching = caching

    def findAndRunQuery(self, name, language=None):
        query = self.findQuery(name)
        results = self.runQuery(query[0], self.results)
        return self.getResults(results)

    def findQuery(self, name, language=None):
        results = []

        for query in self.queries:
            if query.get("name") == name:
                results.append(query)

        return results

    def runQuery(self, query, output):
        """

        output: Dir of
        """
        if self.codeql_exec is None:
            raise Exception("CodeQL binary isn't loaded")

        results = {}

        file_format = "{query_name}-{language}.{format}"

        for database in self.databases:
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
                    self.search_paths[0],
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

                with open(file_output_bqrs_logs, "w") as handle:
                    subprocess.run(command, stdout=handle, stderr=handle)

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
                subprocess.run(command, stdout=handle, stderr=handle)

            results[database.get("language")] = {
                "query_name": query.get("name"),
                "path": file_output_csv,
            }

        return results

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
