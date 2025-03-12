from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_stock import OutletStockManager
import config

def context_menu():
    menu_text = """Co chcesz zrobić?
1. Wystawić produkty outletowe i dograć atrybuty
q żeby wyjść.

Akcja: """
    return str(input(menu_text))


def main():

    while True:
        action = context_menu()

        if action == '1':
            # Create outlet offers
            out_creator = OutletCreator()
            out_creator.connect()
            products_to_publish = out_creator.get_offers_ready_to_publish()
            out_creator.create_outlet_offers(products_to_publish)

            # Move products to lacking
            out_stock_manager = OutletStockManager()
            out_stock_manager.connect()
            out_stock_manager.move_products_to_lacking()

            # Update attribute groups
            out_attribute_manager = OutletAttributeManager()
            out_attribute_manager.connect()
            out_attribute_manager.update_attribute_groups()
            out_attribute_manager.update_main_products_attributes()
        elif action == 'q':
            print('Do zobaczenia!')
            break
        else:
            print('Nie ma takiego wyboru :/')

if __name__ == '__main__':
    main()
