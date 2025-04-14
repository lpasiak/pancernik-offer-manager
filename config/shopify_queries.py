query_product_download = """
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

def get_product_update_mutation(product_id: str, new_title: str) -> str:
    return f"""
    mutation {{
        productUpdate(input: {{
            id: "{product_id}",
            title: "{new_title}"
        }}) {{
            product {{
                id
                title
            }}
            userErrors {{
                field
                message
            }}
        }}
    }}
"""

zapisze_se = 'Robuste Handyhülle für iPhone 14 Plus, Bizon Case Tur, Burgunderrot'