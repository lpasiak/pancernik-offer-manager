from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver
from utils.logger import get_outlet_logger, close_outlet_logger
from utils.mailer import OutletEmailSender

def run_outlet_creator(close_logger=True):
    print('\n----- Creating outlet offers -----\n')
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Creating outlet offers -----<br>')
    out_creator = OutletCreator()
    out_creator.connect()
    number_of_created = out_creator.create_outlet_offers() or 0

    if close_logger:
        log_output = outlet_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        outlet_sender = OutletEmailSender(created=number_of_created,
                                          errors=errors,
                                          operation_logs=log_output)
        outlet_sender.send_emails()
        close_outlet_logger()

    return number_of_created

def run_outlet_empty_checker(close_logger=True):
    print('\n----- Checking for offers not found on Shoper -----\n')
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Checking for offers not found on Shoper -----<br>')
    out_lacking_products_manager = OutletLackingManager()
    out_lacking_products_manager.connect()
    number_of_empty = out_lacking_products_manager.move_products_to_lacking() or 0
    
    if close_logger:
        log_output = outlet_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        outlet_sender = OutletEmailSender(lacking=number_of_empty,
                                          errors=errors,
                                          operation_logs=log_output)
        outlet_sender.send_emails()
        close_outlet_logger()

    return number_of_empty

def run_outlet_discounter(close_logger=True):
    print('\n----- Setting outlet discounts -----\n')
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Setting outlet discounts -----<br>')
    out_discount_manager = OutletDiscountManager()
    out_discount_manager.connect()
    number_of_discounts = out_discount_manager.create_discounts() or 0

    if close_logger:
        log_output = log_output = outlet_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        outlet_sender = OutletEmailSender(discounted=number_of_discounts,
                                          errors=errors,
                                          operation_logs=log_output)
        outlet_sender.send_emails()
        close_outlet_logger()

    return number_of_discounts

def run_outlet_archiver(close_logger=True):
    print('\n----- Deleting and moving sold products to archived -----\n')
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Deleting and moving sold products to archived -----<br>')
    out_archiver = OutletArchiver()
    out_archiver.connect()
    products_sold_to_archive, products_to_activate, products_to_deactivate = out_archiver.categorize_products()

    number_of_archived = out_archiver.archive_sold_products(products_sold_to_archive) or 0
    # Disabled for now (need to figure out how to ameliorate the function, it doesn't make sense rn)
    # number_of_activated = out_archiver.reactivate_products(products_to_activate) or 0
    number_of_activated = 0
    number_of_deactivated = out_archiver.deactivate_products(products_to_deactivate) or 0

    if close_logger:
        log_output = outlet_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        outlet_sender = OutletEmailSender(archived=number_of_archived,
                                          activated=number_of_activated,
                                          deactivated=number_of_deactivated,
                                          errors=errors,
                                          operation_logs=log_output)
        outlet_sender.send_emails()
        close_outlet_logger()

    return number_of_archived, number_of_activated, number_of_deactivated

def run_outlet_attributer(close_logger=True):
    print('\n----- Updating outlet attributes -----\n')
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Updating outlet attributes -----<br>')
    out_attribute_manager = OutletAttributeManager()
    out_attribute_manager.connect()
    number_of_attribute_groups = out_attribute_manager.update_attribute_groups() or 0
    number_of_attributes_main = out_attribute_manager.update_main_products_attributes() or 0

    if close_logger:
        log_output = outlet_log_manager.get_log_as_string()
        errors = log_output.count('❌')
        outlet_sender = OutletEmailSender(attributes=number_of_attributes_main,
                                          category_attributes=number_of_attribute_groups,
                                          errors=errors,
                                          operation_logs=log_output)
        outlet_sender.send_emails()
        close_outlet_logger()

    return number_of_attribute_groups, number_of_attributes_main
        
def run_outlet_manager():
    outlet_log_manager = get_outlet_logger()
    outlet_logger = outlet_log_manager.get_logger()
    outlet_logger.info('<br>----- Outlet Manager -----<br>')

    created_offers = run_outlet_creator(close_logger=False)
    lacking_offers = run_outlet_empty_checker(close_logger=False)
    discounted_offers = run_outlet_discounter(close_logger=False)
    archived_offers, activated_offers, deactivated_offers = run_outlet_archiver(close_logger=False)
    attribute_groups, attribute_main = run_outlet_attributer(close_logger=False)
    
    log_output = outlet_log_manager.get_log_as_string()
    errors = log_output.count('❌')
    outlet_sender = OutletEmailSender(created=created_offers,
                                      lacking=lacking_offers,
                                      discounted=discounted_offers,
                                      archived=archived_offers,
                                      activated=activated_offers,
                                      deactivated=deactivated_offers,
                                      category_attributes=attribute_groups,
                                      attributes=attribute_main,
                                      errors=errors,
                                      operation_logs=log_output)
    outlet_sender.send_emails()
    close_outlet_logger()
