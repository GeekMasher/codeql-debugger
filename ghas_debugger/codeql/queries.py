import os
import logging
import subprocess

QUERIES_PATH = os.path.join(os.getcwd(), "queries")
RESULTS_PATH = os.path.join(os.getcwd(), "results")

QUERIES = {
    "lines_of_code": "LinesOfCode",
    # "commented_code": "LinesOfCommentedCode",
    # "commented": "LinesOfComment",
    # "tests": "NumberOfTests"
}


class Queries:
    def __init__(
        self,
        languages=[],
        results: str = RESULTS_PATH,
        queries_path: str = QUERIES_PATH,
        database: str = None,
        codeql_bin: str = None
    ):
        self.queries_path = queries_path
        self.languages = languages
        self.codeql_bin = codeql_bin
        self.database = database

        self.data = {}

        self.results = results
        if not os.path.exists(self.results):
            logging.debug("Creating results dir :: " + self.results)
            os.makedirs(self.results)

    def findQueryLocation(self, path, language):
        query_dir = os.path.join(self.queries_path, language)
        if not os.path.exists(query_dir):
            raise Exception("Unknown Query Directory")

        if not path.endswith(".ql"):
            path = path + ".ql"

        query_file = os.path.join(query_dir, path)
        if not os.path.exists(query_file):
            raise Exception("Unknown Query File location :: " + query_file)

        return query_file

    def runQuery(self, query, output):
        if self.codeql_bin is None:
            raise Exception("CodeQL binary isn't loaded")

        command = [
            self.codeql_bin, "database", "analyze",
            '--search-path', './queries/',
            '--format', 'csv',
            '--output', output,
            self.database,
            query
        ]
        """
        ./bin/codeql-cli/codeql database upgrade \
        --search-path=./queries/ \
        --search-path=./queries/ \
        ./databases/$NAME

        ./bin/codeql-cli/codeql database analyze \
            --ram=8000 --threads=4 \
            --search-path=./queries/ \
            --format="sarif-latest" \
            --output="./results/$NAME-query.sarif" \
            ./databases/$NAME \
            queries/custom/javascript/HardcodedPassword.ql
        """

        logging.debug("CodeQL Command :: " + str(command))

        print(' '.join(command))

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
