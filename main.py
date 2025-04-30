from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver
from export_manager.export_manager import ExportManagerShoper, ExportManagerShopify, ExpportManagerEasyStorage
from promo_manager.promo_manager import PromoManager
from bundle_manager.bundle_manager import BundleManager
from connections.shopify.products import ShopifyProducts
from connections.shopify_connect import ShopifyAPIClient
from connections.idosell_connect import IdoSellAPIClient
from connections.idosell.products import IdoSellProducts
import config

def main():

    # Main program
    while True:
        action = config.context_menu()

        # Export manager
        if action == '0':
            action = config.context_menu_export()

            if action == '1':
                shoper_export_manager = ExportManagerShoper()
                shoper_export_manager.connect()
                shoper_export_manager.export_all_data_from_shoper()
                break

            if action == '2':
                shopify_export_manager = ExportManagerShopify()
                shopify_export_manager.connect()
                shopify_export_manager.export_shopify_products_light()
                break

            if action == '3':
                shopify_export_manager = ExportManagerShopify()
                shopify_export_manager.connect()
                shopify_export_manager.export_shopify_products_bizon()
                break

            if action == '4':
                easystorage_export_manager = ExpportManagerEasyStorage()
                easystorage_export_manager.connect()
                easystorage_export_manager.export_wms_pancernik_products()
                break

            if action == '5':
                easystorage_export_manager = ExpportManagerEasyStorage()
                easystorage_export_manager.connect()
                easystorage_export_manager.export_wms_bizon_products()
                break


            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
        
            else:
                print('Nie ma takiego wyboru :/')

        # Outlet manager
        if action == '1':
            action = config.context_menu_outlet()
            if action == '1':
                # Create outlet offers
                out_creator = OutletCreator()
                out_creator.connect()
                products_to_publish = out_creator.get_offers_ready_to_publish()
                out_creator.create_outlet_offers(products_to_publish)

                # Move products to lacking
                out_lacking_products_manager = OutletLackingManager()
                out_lacking_products_manager.connect()
                out_lacking_products_manager.move_products_to_lacking()

            elif action == '2':
                # Create discounts
                out_discount_manager = OutletDiscountManager()
                out_discount_manager.connect()
                products_to_discount = out_discount_manager.select_products_to_discount()
                out_discount_manager.create_discounts(products_to_discount)

            elif action == '3':
                # Remove products that have been sold
                out_archiver = OutletArchiver()
                out_archiver.connect()
                products_sold_to_archive = out_archiver.select_sold_products()
                out_archiver.archive_sold_products(products_sold_to_archive)

            elif action == '4':
                # Update attribute groups
                out_attribute_manager = OutletAttributeManager()
                out_attribute_manager.connect()
                out_attribute_manager.update_attribute_groups()
                out_attribute_manager.update_main_products_attributes()

            elif action == 'test':
                # Remove products that have been sold
                out_archiver = OutletArchiver()
                out_archiver.connect()
                products_sold_to_archive = out_archiver.select_sold_products()
                print(products_sold_to_archive)
                products_sold_to_archive.to_excel('testowy.xlsx')

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

            if action == '3':
                promo_manager.update_product_stock_from_gsheet()
    
            if action == '4':
                promo_manager.remove_promo_offers_from_gsheet()

            if action == '5':
                promo_manager.import_promo_fixed_from_gsheet()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

        # Bundle manager
        elif action == '3':
            action = config.context_menu_bundle()
            bundle_manager = BundleManager()
            bundle_manager.connect()
            
            if action == '1':
                bundle_manager.create_a_bundle('5904665389942', '5907339019107')

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
            idosell_client = IdoSellAPIClient(api_key=config.IDOSELL_API_KEY, site=config.IDOSELL_BIZON_B2B_SITE)
            idosell_client.connect()
            idosell_products = IdoSellProducts(idosell_client)

            if action == '1':
                idosell_products.get_all_products()

            if action == '2':
                idosell_products = IdoSellProducts(idosell_client)
                idosell_products.add_stock_price(price=9.44, external_code='BCTMG555GBK')

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
