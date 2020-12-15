import os
import glob
import logging


def getDatabases(roots: list, name: str = None):
    results = []

    for root in roots:
        if root == "":
            continue
        if not os.path.exists(root) and not os.path.isdir(root):
            logging.warning("Database file does not exists :: `" + str(root) + "`")
            continue

        logging.info("Loading CodeQL Database Path :: " + root)

        for database_name in os.listdir(root):
            database_path = os.path.join(root, database_name)
            if not os.path.isdir(database_path):
                continue

            # TODO: More testing
            codeql_db_yml = os.path.join(database_path, "codeql-database.yml")
            if not os.path.exists(codeql_db_yml):
                logging.debug("CodeQL Database yml file not present")
                continue

            # Filter if name supplied
            if name and name != database_name:
                continue

            db_paths = os.path.basename(glob.glob(database_path + "/db-*")[0])
            language = db_paths.replace("db-", "")
            logging.debug("CodeQL Database Language :: " + language)

            logging.debug("Found Database folder :: " + database_path)
            results.append(
                {"name": database_name, "path": database_path, "language": language}
            )

    return results
