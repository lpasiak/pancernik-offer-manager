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
                                compareAtPrice
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
                    vendor
                    descriptionHtml
                    variants(first: 2) {
                        edges {
                            node {
                                sku
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

def mutation_product_update_url(product_id: str, handle: str, title: str, descriptionHtml: str) -> str:
    # Escape any quotes in the HTML content
    descriptionHtml = descriptionHtml.replace('"', '\\"').replace('\n', '\\n')
    
    return f"""
    mutation {{
        productUpdate(input: {{
            id: "{product_id}",
            title: "{title}",
            descriptionHtml: "{descriptionHtml}",
            handle: "{handle}",
            redirectNewHandle: true
        }}) {{
            product {{
                id
                handle
                title
                descriptionHtml
            }}
            userErrors {{
                field
                message
            }}
        }}
    }}
"""
