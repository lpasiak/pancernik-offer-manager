from connections.gsheets_connect import GSheetsClient
from outlet_manager.outlet_manager import OutletManager

def main():
    
    out_manager = OutletManager()
    out_manager.connect()
    products_to_publish = out_manager.get_offers_ready_to_publish()
    out_manager.create_outlet_offers(products_to_publish)

if __name__ == '__main__':
    main()
