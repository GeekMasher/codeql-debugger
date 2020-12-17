QUERY_TEST = """\
{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""

QUERY_DEPENDENCIES = """\
query ($organizationName: String!, $repositoryName: String!, $cursor: String){
  repository(owner: $organizationName name: $repositoryName) {
    name
    dependencyGraphManifests(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
      edges {
        node {
          filename
          dependenciesCount
          blobPath
          exceedsMaxSize
          parseable
          dependencies{
            edges {
              node {
                packageName
                packageManager
                requirements
              }
            }
          }
        }
      }
    }
  }
}
"""
