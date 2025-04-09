from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver
from export_manager.export_manager import ExportManagerShoper, ExportManagerShopify
from promo_manager.promo_manager import PromoManager
from bundle_manager.bundle_manager import BundleManager


def context_menu():
    menu_text = """--------------------------------
Z czym dziś chcesz pracować?
0. Pobrać informacje o produktach
1. Menedżer outletów
2. Menedżer promocji
3. Menedżer zestawów
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_outlet():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Wystawić outlety
2. Obniżki na outlety
3. Przenieść sprzedane/archiwalne
4. Atrybuty produktów
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_promo():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Pobrać promocje
2. Zaimportować promocje
3. Uaktualnić stany magazynowe
4. Usunąć promocje
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_bundle():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Utworzyć zestaw
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_easystorage():
    menu_text = """--------------------------------
Czy wyeksportowałeś i zapisałeś plik z EasyStorage? (y/n)
Akcja: """
    return str(input(menu_text))

def context_menu_export():
    menu_text = """--------------------------------
Skąd chcesz pobrać dane?
1. Shoper
2. Shopify
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def main():

    # Main program
    while True:
        action = context_menu()

        # Export manager
        if action == '0':
            action = context_menu_export()

            if action == '1':
                shoper_export_manager = ExportManagerShoper()
                shoper_export_manager.connect()
                shoper_export_manager.export_all_data_from_shoper()
                break

            if action == '2':
                shopify_export_manager = ExportManagerShopify()
                shopify_export_manager.connect()
                shopify_export_manager.export_shopify_products()
                break

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
        
            else:
                print('Nie ma takiego wyboru :/')

        # Outlet manager
        if action == '1':
            action = context_menu_outlet()
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
                # Remove products that have been sold or haven't sold for 6 weeks
                action = context_menu_easystorage()

                if action == 'y':
                    out_archiver = OutletArchiver()
                    out_archiver.connect()
                    products_sold_to_archive = out_archiver.select_sold_products()
                    out_archiver.archive_sold_products(products_sold_to_archive)

                elif action == 'n':
                    print('Pobierz plik z EasyStorage i zapisz go jako Easystorage.xlsx w folderze "sheets"')

                elif action.lower() == 'q':
                    print('Do zobaczenia!')
                    break
            
                else:
                    print('Nie ma takiego wyboru :/')

            elif action == '4':
                # Update attribute groups
                out_attribute_manager = OutletAttributeManager()
                out_attribute_manager.connect()
                out_attribute_manager.update_attribute_groups()
                out_attribute_manager.update_main_products_attributes()

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
            else:
                print('Nie ma takiego wyboru :/')

        # Promo manager
        elif action == '2':
            action = context_menu_promo()
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

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
            
        elif action.lower() == 'q':
                print('Do zobaczenia!')
                break

        # Bundle manager
        elif action == '3':
            action = context_menu_bundle()
            bundle_manager = BundleManager()
            bundle_manager.connect()
            
            if action == '1':
                bundle_manager.create_a_bundle('5904665389942', '5907339019107')

            elif action.lower() == 'q':
                print('Do zobaczenia!')
                break
            else:
                print('Nie ma takiego wyboru :/')

if __name__ == '__main__':
    main()
