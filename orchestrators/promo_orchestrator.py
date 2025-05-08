from promo_manager.promo_manager import PromoManager

def run_promo_remover():
    promo_manager = PromoManager()
    promo_manager.connect()
    promo_manager.remove_promo_offers_from_gsheet()
    
def run_percent_promo_and_stock_importer():
    promo_manager = PromoManager()
    promo_manager.connect()
    promo_manager.import_promo_percent_from_gsheet()
    promo_manager.update_product_stock_from_gsheet()

def run_fixed_promo_importer():
    promo_manager = PromoManager()
    promo_manager.connect()
    promo_manager.import_promo_fixed_from_gsheet()

def run_promo_exporter():
    promo_manager = PromoManager()
    promo_manager.connect()
    promo_manager.export_all_promo_products()

def run_promo_manager():
    run_promo_remover()
    run_percent_promo_and_stock_importer()
    run_fixed_promo_importer()
    run_promo_exporter()