import os
import logging
import subprocess


class Queries:
    def __init__(
        self,
        languages=[],
        results: str = None,
        queries_path: str = None,
        databases: list = None,
        codeql: str = None,
    ):
        self.queries_path = queries_path
        self.languages = languages
        self.codeql_exec = codeql
        self.databases = databases

        self.data = {}

        self.results = results
        if not os.path.exists(self.results):
            logging.debug("Creating results dir :: " + self.results)
            os.makedirs(self.results)

    def getQueriesList(self, language=None):
        query_files = [
            os.path.join(dp, f)
            for dp, dn, filenames in os.walk(self.queries_path)
            for f in filenames
            if os.path.splitext(f)[1] == ".ql"
        ]

        results = []
        for query in query_files:
            lang = os.path.split(query.replace(self.queries_path, ""))[0]

            # if language and language != lang:
            #     continue

            results.append(
                {
                    "name": os.path.splitext(os.path.basename(query))[0],
                    "path": query,
                    "language": lang.replace("/", ""),
                }
            )

        return results

    def findQuery(self, name, language=None):
        results = []

        for query in self.getQueriesList(language=language):
            if query.get("name") == name:
                results.append(query)

        return results

    def runQuery(self, query, output):
        if self.codeql_exec is None:
            raise Exception("CodeQL binary isn't loaded")

        for database in self.databases:
            command = [
                self.codeql_exec,
                "database",
                "analyze",
                "--search-path",
                "./queries/",
                "--format",
                "csv",
                "--output",
                output,
                database.get("path"),
                query.get("path"),
            ]

            logging.debug("CodeQL Command :: " + str(command))

            print(" ".join(command))

            subprocess.run(command)

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
