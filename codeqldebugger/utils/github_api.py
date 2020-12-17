import logging
import requests
from string import Template

from codeqldebugger.utils.github_api_queries import *


class GitHubAPI:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint

        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer " + token})

        self.active = self.check()

    def callGraphQL(self, query, arguments={}):
        logging.debug("GitHubAPI - Performing call to GraphQL API")

        query_template = Template(query)
        query = query_template.substitute(cursor="0", **arguments)

        request = self.session.post(
            self.endpoint, json={"query": query, "variables": arguments}
        )

        if request.status_code == 200:
            data = request.json()

            if data.get("errors"):
                error = data.get("errors", [])[0].get("message")
                logging.error(error)

            return data
        else:
            raise Exception(
                "Query failed to run by returning code of {}. {}".format(
                    request.status_code, query
                )
            )

    def check(self):
        logging.info("Checking GitHub API")
        try:
            result = self.callGraphQL(QUERY_TEST)
            # Print rate limit
            rrl = result["data"]["rateLimit"]["remaining"]
            logging.debug("GitHub API - Rate Limit remaining :: " + str(rrl))

            return True
        except Exception as error:
            logging.error("GitHub API test failed")
            return False

    def getDependancies(self, org, repo):
        return self.callGraphQL(
            QUERY_DEPENDENCIES,
            arguments={"organizationName": org, "repositoryName": repo},
        )
