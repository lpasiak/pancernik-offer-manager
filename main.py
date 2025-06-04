import orchestrators.outlet_orchestrator as outlet
import orchestrators.export_orchestrator as export
import orchestrators.promo_orchestrator as promo
from bundle_manager.bundle_manager import BundleManager
from connections.shopify.products import ShopifyProducts
from connections.shopify_connect import ShopifyAPIClient
from connections import AllegroAPIClient
from connections.allegro.offers import AllegroOffers
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

            elif action =='7':
                # Export Shoper Beautiful Products
                export.run_shoper_bautiful_products_exporter()
                
            elif action == 'all':
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
                # Remove old redirects
                outlet.run_redirects_remover()

            elif action == '4':
                # Remove products that have been sold
                outlet.run_outlet_archiver()

            elif action == '5':
                # Update attribute groups
                outlet.run_outlet_attributer()

            elif action == 'all':
                # Do all the steps
                outlet.run_outlet_manager()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
            else:
                print('Nie ma takiego wyboru :/')

        # ----- Promo manager ------ #
        elif action == '2':
            action = config.context_menu_promo()

            if action == '1':
                # Remove promotions
                promo.run_promo_remover()

            elif action == '2':
                # Import promotions percent and stocks
                promo.run_percent_promo_and_stock_importer()
    
            elif action == '3':
                # Import promotions fixed
                promo.run_fixed_promo_importer()

            elif action == '4':
                # Manage promotions, comparing them to the existent Allegro discounts
                promo.run_allegro_discount_comparator()

            elif action == '5':
                # Export promotions
                promo.run_promo_exporter()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

            else:
                print('Nie ma takiego wyboru :/')

        # ----- Bundle manager ------ #
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

        # ----- Shopify manager ------ #
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

        # ----- IdoSell manager ------ #
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

        # ----- IdoSell manager ------ #
        elif action == '6':
            action = config.context_menu_allegro()
            allegro_client = AllegroAPIClient()
            allegro_client.connect()
            allegro_offers = AllegroOffers(allegro_client)

            if action == '1':
                allegro_offers.get_an_offer_by_id(7778626016)
            
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
