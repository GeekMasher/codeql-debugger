
import os
import logging


def getDatabases(root, name=None):
    logging.info("Loading CodeQL Database Path :: " + root)

    results = []
    for database_name in os.listdir(root):
        database_path = os.path.join(root, database_name)
        if not os.path.isdir(database_path):
            continue

        # TODO: More testing 

        logging.debug('Found Database folder :: ' + database_path)
        results.append({
            "name": database_name,
            "path": database_path
        })

    return results
