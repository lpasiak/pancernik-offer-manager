from export_manager.export_manager import (
    ExportManagerShoper, 
    ExportManagerShopify, 
    ExpportManagerEasyStorage, 
    ExportManagerIdosell
)

def run_shoper_exporter():
    print('\n----- ℹ️  Exporting Shoper Information -----\n')
    shoper_export_manager = ExportManagerShoper()
    shoper_export_manager.connect()
    shoper_export_manager.export_all_data_from_shoper()

def run_shopify_light_exporter():
    print('\n----- ℹ️  Exporting Shopify Light Products -----\n')
    shopify_export_manager = ExportManagerShopify()
    shopify_export_manager.connect()
    shopify_export_manager.export_shopify_products_light()

def run_shopify_bizon_exporter():
    print('\n----- ℹ️  Exporting Shopify Bizon Products -----\n')
    shopify_export_manager = ExportManagerShopify()
    shopify_export_manager.connect()
    shopify_export_manager.export_shopify_products_bizon()

def run_pancernik_easystorage_exporter():
    print('\n----- ℹ️  Exporting EasyStorage Pancernik Products -----\n')
    easystorage_export_manager = ExpportManagerEasyStorage()
    easystorage_export_manager.connect()
    easystorage_export_manager.export_wms_pancernik_products()

def run_bizon_easystorage_exporter():
    print('\n----- ℹ️  Exporting EasyStorage Bizon Products -----\n')
    easystorage_export_manager = ExpportManagerEasyStorage()
    easystorage_export_manager.connect()
    easystorage_export_manager.export_wms_bizon_products()

def run_idosell_exporter():
    print('\n----- ℹ️  Exporting IdoSell Products -----\n')
    idosell_export_manager = ExportManagerIdosell()
    idosell_export_manager.connect()
    idosell_export_manager.export_idosell_products_descriptions()

def run_massive_exporter():
    run_shoper_exporter()
    run_shopify_light_exporter()
    run_shopify_bizon_exporter()
    run_pancernik_easystorage_exporter()
    run_bizon_easystorage_exporter()
    run_idosell_exporter()