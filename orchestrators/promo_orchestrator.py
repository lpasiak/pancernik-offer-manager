from promo_manager.promo_manager import PromoManager
from utils.logger import get_promo_logger, close_promo_logger
from utils.mailer import PromoEmailSender
import config


def run_promo_remover(close_logger=True):
    promo_manager = PromoManager(sheet_id=config.PROMO_SHEET_ID)
    promo_manager.connect()
    promo_manager.remove_promo_offers_from_gsheet()
    
def run_percent_promo_and_stock_importer(close_logger=True):
    promo_manager = PromoManager(sheet_id=config.PROMO_SHEET_ID)
    promo_manager.connect()
    promo_manager.import_promo_percent_from_gsheet()
    promo_manager.update_product_stock_from_gsheet()

def run_fixed_promo_importer(close_logger=True):
    promo_manager = PromoManager(sheet_id=config.PROMO_SHEET_ID)
    promo_manager.connect()
    promo_manager.import_promo_fixed_from_gsheet()

def run_allegro_discount_comparator(close_logger=True):
    promo_log_manager = get_promo_logger()
    promo_logger = promo_log_manager.get_logger()

    print('\n----- Creating discounts -----\n')
    promo_logger.info('<br>----- Creating discounts -----<br>')

    promo_manager = PromoManager(sheet_id=config.ALLEGRO_PROMO_SHEET_ID)
    promo_manager.connect()
    discounts_created, discounts_ommited, discounts_too_early, discounts_failed = promo_manager.allegro_discount_offers()
    discounts_removed = promo_manager.allegro_discount_offers_remover()

    if close_logger:
        log_output = promo_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        promo_sender = PromoEmailSender(created_promo_allegro=discounts_created,
                                        ommited_promo_allegro=discounts_ommited,
                                        ommited_promo_allegro_early=discounts_too_early,
                                        discounts_failed=discounts_failed,
                                        removed_promo_allegro=discounts_removed,
                                        errors=errors,
                                        operation_logs=log_output)
        promo_sender.send_emails()
        close_promo_logger()

def run_promo_exporter(close_logger=True):
    promo_manager = PromoManager(sheet_id=config.PROMO_SHEET_ID)
    promo_manager.connect()
    promo_manager.export_all_promo_products()

def run_promo_manager():
    run_promo_remover(close_logger=False)
    run_percent_promo_and_stock_importer(close_logger=False)
    run_fixed_promo_importer(close_logger=False)
    # run_allegro_discount_comparator(close_logger=False)
    run_promo_exporter(close_logger=False)
