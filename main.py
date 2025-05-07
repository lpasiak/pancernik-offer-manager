import orchestrators.outlet_orchestrator as outlet
import orchestrators.export_orchestrator as export
from export_manager.export_manager import ExportManagerShoper, ExportManagerShopify, ExpportManagerEasyStorage, ExportManagerIdosell
from promo_manager.promo_manager import PromoManager
from bundle_manager.bundle_manager import BundleManager
from connections.shopify.products import ShopifyProducts
from connections.shopify_connect import ShopifyAPIClient
from idosell_manager.idosell_manager import IdoSellManager
import config

def main():

    while True:
        action = config.context_menu()

        # ----- Export manager ------ #
        if action == '0':
            action = config.context_menu_export()

            if action == '1':
                # Export Shoper items
                export.run_shoper_exporter()

            elif action == '2':
                # Export Shopify Light products
                export.run_shopify_light_exporter()

            elif action == '3':
                # Export Shopify Bizon products
                export.run_shopify_bizon_exporter()

            elif action == '4':
                # Export EasyStorage Pancernik products
                export.run_pancernik_easystorage_exporter()

            elif action == '5':
                # Export EasyStorage Bizon products
                export.run_bizon_easystorage_exporter()

            elif action == '6':
                # Export IdoSell products
                export.run_idosell_exporter()

            elif action == 'wszycho':
                # Do all the steps
                export.run_massive_exporter()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
        
            else:
                print('Nie ma takiego wyboru :/')

        # ----- Outlet manager ------ #
        if action == '1':
            action = config.context_menu_outlet()

            if action == '1':
                # Create outlet offers
                outlet.run_outlet_creator()
                # Move products to lacking
                outlet.run_outlet_empty_checker

            elif action == '2':
                # Create discounts
                outlet.run_outlet_discounter()

            elif action == '3':
                # Remove products that have been sold
                outlet.run_outlet_archiver()

            elif action == '4':
                # Update attribute groups
                outlet.run_outlet_attributer()

            elif action == 'wszycho':
                # Do all the steps
                outlet.run_outlet_manager()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
            else:
                print('Nie ma takiego wyboru :/')

        # Promo manager
        elif action == '2':
            action = config.context_menu_promo()
            promo_manager = PromoManager()
            promo_manager.connect()

            if action == '1':
                promo_manager.export_all_promo_products()

            if action == '2':
                promo_manager.import_promo_percent_from_gsheet()
                promo_manager.update_product_stock_from_gsheet()
    
            if action == '3':
                promo_manager.remove_promo_offers_from_gsheet()

            if action == '4':
                promo_manager.import_promo_fixed_from_gsheet()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

            else:
                print('Nie ma takiego wyboru :/')

        # Bundle manager
        elif action == '3':
            action = config.context_menu_bundle()
            bundle_manager = BundleManager()
            bundle_manager.connect()
            
            if action == '1':
                bundle_manager.download_bundled_case_images()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

            else:
                print('Nie ma takiego wyboru :/')

        elif action == '4':
            action = config.context_menu_shopify()

            if action == '1':
                shopify_client = ShopifyAPIClient(
                    shop_url=config.SHOPIFY_CREDENTIALS['shop_url'],
                    api_version=config.SHOPIFY_API_VERSION,
                    api_token=config.SHOPIFY_CREDENTIALS['api_token'])
            
                shopify_client.connect()
                shopify_products = ShopifyProducts(shopify_client)
                shopify_products.update_products_urls()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

            else:
                print('Nie ma takiego wyboru :/')

        elif action == '5':
            action = config.context_menu_idosell()
            idosell_manager = IdoSellManager()
            idosell_manager.connect()

            if action == '1':
                idosell_manager.upload_product_information()
            
            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

            else:
                print('Nie ma takiego wyboru :/')

        # Exit the program
        elif action.lower() == 'q':
            print('Do zobaczenia!')
            break

if __name__ == '__main__':
    main()
