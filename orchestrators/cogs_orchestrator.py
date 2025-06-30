from google_feed_manager import GoogleCostOfGoodsSold

def update_missing_cogs():
    google_cogs = GoogleCostOfGoodsSold()
    google_cogs.connect()

    product_df = google_cogs.get_all_products_from_shoper_export()

    google_cogs.import_bizon_prices_to_shoper(product_df)
    google_cogs.import_bewood_dropshipping_prices_to_shoper(product_df)
    google_cogs.import_grizz_dropshipping_prices_to_shoper(product_df)
