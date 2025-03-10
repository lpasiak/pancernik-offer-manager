from connections.gsheets_connect import GSheetsClient
from outlet_manager.outlet_manager import OutletManager
import config

def main():
    
    out_manager = OutletManager()
    if out_manager.connect():
        out_manager.get_offers_ready_to_publish()

if __name__ == '__main__':
    main()
