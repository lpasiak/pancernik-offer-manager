query_product_light = """
    {
        products(
            first: 250  # Maximum allowed per request
            after: null  # Will be updated for pagination
        ) {
            edges {
                node {
                    id
                    title
                    handle
                    variants(first: 2) {
                        edges {
                            node {
                                sku
                                barcode
                                price
                            }
                        }
                    }
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

query_product_bizon = """
    {
        products(
            first: 250  # Maximum allowed per request
            query: "vendor:Bizon"  # Filter by vendor
            after: null  # Will be updated for pagination
        ) {
            edges {
                node {
                    id
                    title
                    handle
                    variants(first: 2) {
                        edges {
                            node {
                                sku
                                barcode
                                price
                            }
                        }
                    }
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

def mutation_product_update_url(product_id: str, new_url: str) -> str:
    return f"""
    mutation {{
        productUpdate(input: {{
            id: "{product_id}",
            handle: "{new_url}",
            redirectNewHandle: true
        }}) {{
            product {{
                id
                handle
            }}
            userErrors {{
                field
                message
            }}
        }}
    }}
"""
