import os
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
    ):
        self.queries = queries
        self.languages = languages
        self.codeql_exec = codeql
        self.databases = databases
        self.search_paths = search_paths

        self.data = {}

        self.results = results
        if not os.path.exists(self.results):
            logging.debug("Creating results dir :: " + self.results)
            os.makedirs(self.results)

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

        multi_language = True if len(self.databases) < 1 else False

        file_format = "{query_name}-{language}.{format}"

        for database in self.databases:
            file_output_bqrs = os.path.join(
                output,
                file_format.format(
                    query_name=query.get("name"),
                    language=database.get("language"),
                    format="bqrs",
                ),
            )

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

            with open(file_output_bqrs + ".log", "w") as handle:
                subprocess.run(command, stdout=handle, stderr=handle)

            # BQRS to format
            file_output_csv = os.path.join(
                output,
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

            print(" ".join(command))
            # TODO: Pipe output
            with open(file_output_csv + ".log", "w") as handle:
                subprocess.run(command, stdout=handle, stderr=handle)

        return output

    def runQueries(self):
        for query_name, query_path in QUERIES.items():
            logging.info("Loading Query :: " + query_name)

            self.data[query_name] = {}

            for language in self.languages:
                query_path = self.findQueryLocation(query_path, language)

                output_path = os.path.join(
                    self.results, language + "-" + query_name + ".csv"
                )

                self.data[query_name][language] = self.runQuery(query_path, output_path)

        return self.data
