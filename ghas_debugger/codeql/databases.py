import os
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

            if name and name != database_name:
                continue

            logging.debug("Found Database folder :: " + database_path)
            results.append({"name": database_name, "path": database_path})

    return results
