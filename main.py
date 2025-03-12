from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
import config

def context_menu():
    menu_text = """Co chcesz zrobić?
1. Wystawić produkty outletowe
2. Dograć atrybuty do produktów
q żeby wyjść.

Akcja: """
    return str(input(menu_text))


def main():

    while True:
        action = context_menu()

        if action == '1':
            out_creator = OutletCreator()
            out_creator.connect()
            products_to_publish = out_creator.get_offers_ready_to_publish()
            out_creator.create_outlet_offers(products_to_publish)
        elif action == '2':
            out_attribute_manager = OutletAttributeManager()
            out_attribute_manager.connect()
            out_attribute_manager.update_attribute_groups()
        elif action == 'q':
            print('Do zobaczenia!')
            break
        else:
            print('Nie ma takiego wyboru :/')

if __name__ == '__main__':
    main()
