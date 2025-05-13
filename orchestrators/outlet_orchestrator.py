from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver
from utils.logger import get_outlet_logger, close_outlet_logger

def run_outlet_creator(close_logger=True):
    print('\n----- Creating outlet offers -----\n')
    get_outlet_logger().info('<br>----- Creating outlet offers -----<br>')
    out_creator = OutletCreator()
    out_creator.connect()
    products_to_publish = out_creator.get_offers_ready_to_publish()
    out_creator.create_outlet_offers(products_to_publish)

    if close_logger:
        close_outlet_logger()

def run_outlet_empty_checker(close_logger=True):
    print('\n----- Checking for offers not found on Shoper -----\n')
    get_outlet_logger().info('<br>----- Checking for offers not found on Shoper -----<br>')
    out_lacking_products_manager = OutletLackingManager()
    out_lacking_products_manager.connect()
    out_lacking_products_manager.move_products_to_lacking()

    if close_logger:
        close_outlet_logger()

def run_outlet_discounter(close_logger=True):
    print('\n----- Setting outlet discounts -----\n')
    get_outlet_logger().info('<br>----- Setting outlet discounts -----<br>')
    out_discount_manager = OutletDiscountManager()
    out_discount_manager.connect()
    products_to_discount = out_discount_manager.select_products_to_discount()
    out_discount_manager.create_discounts(products_to_discount)

    if close_logger:
        close_outlet_logger()

def run_outlet_archiver(close_logger=True):
    print('\n----- Deleting and moving sold products to archived -----\n')
    get_outlet_logger().info('<br>----- Deleting and moving sold products to archived -----<br>')
    out_archiver = OutletArchiver()
    out_archiver.connect()
    products_sold_to_archive = out_archiver.select_sold_products()
    out_archiver.archive_sold_products(products_sold_to_archive)

    if close_logger:
        close_outlet_logger()

def run_outlet_attributer(close_logger=True):
    print('\n----- Updating outlet attributes -----\n')
    get_outlet_logger().info('<br>----- Updating outlet attributes -----<br>')
    out_attribute_manager = OutletAttributeManager()
    out_attribute_manager.connect()
    out_attribute_manager.update_attribute_groups()
    out_attribute_manager.update_main_products_attributes()

    if close_logger:
        close_outlet_logger()

def run_outlet_manager():
    run_outlet_creator(close_logger=False)
    run_outlet_empty_checker(close_logger=False)
    run_outlet_discounter(close_logger=False)
    run_outlet_archiver(close_logger=False)
    run_outlet_attributer(close_logger=False)
    
    close_outlet_logger()
