import os
import glob
import logging


def getDatabases(roots: list, name: str = None):
    results = []

    if not name:
        logging.debug("No filtering using `name`")

    for root in roots:
        if root == "":
            continue
        if not os.path.exists(root) and not os.path.isdir(root):
            logging.warning("Database file does not exists :: `" + str(root) + "`")
            continue

        logging.info("Loading CodeQL Database Path :: " + root)

        database_paths = os.listdir(root)
        if len(database_paths) == 0:
            logging.debug("No Database folder sub-dirs were found")

        for database_name in database_paths:
            database_path = os.path.join(root, database_name)
            if not os.path.isdir(database_path):
                logging.debug("Database path is not a dir :: " + database_path)
                continue

            # Test if the folder is a CodeQL DB folder
            codeql_db_yml = os.path.join(database_path, "codeql-database.yml")
            if not os.path.exists(codeql_db_yml):
                logging.debug("CodeQL Database yml file not present")
                continue

            # Filter if name supplied
            if name and name != database_name:
                logging.debug("Ignore database :: " + database_name)
                continue

            db_paths = glob.glob(database_path + "/db-*")
            if len(db_paths) == 0:
                logging.debug("No CodeQL `db-*` folder found")
                continue
            db_paths = os.path.basename(db_paths[0])

            language = db_paths.replace("db-", "")
            logging.debug("CodeQL Database Language :: " + language)

            logging.info("Found Database folder :: " + database_path)
            results.append(
                {"name": database_name, "path": database_path, "language": language}
            )

    return results
