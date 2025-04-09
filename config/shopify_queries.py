download_products_query = """
    {
        products(
            first: 250  # Maximum allowed per request
            after: null  # Will be updated for pagination
        ) {
            edges {
                node {
                    id
                    title
                }
                cursor
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
"""