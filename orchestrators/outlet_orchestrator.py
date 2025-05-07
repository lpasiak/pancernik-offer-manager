from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver

def run_outlet_creator():
    print('\n----- ℹ️  Creating outlet offers -----\n')
    out_creator = OutletCreator()
    out_creator.connect()
    products_to_publish = out_creator.get_offers_ready_to_publish()
    out_creator.create_outlet_offers(products_to_publish)

def run_outlet_empty_checker():
    print('\n----- ℹ️  Checking for offers not found on Shoper -----\n')
    out_lacking_products_manager = OutletLackingManager()
    out_lacking_products_manager.connect()
    out_lacking_products_manager.move_products_to_lacking()

def run_outlet_discounter():
    print('\n----- ℹ️  Setting outlet discounts -----\n')
    out_discount_manager = OutletDiscountManager()
    out_discount_manager.connect()
    products_to_discount = out_discount_manager.select_products_to_discount()
    out_discount_manager.create_discounts(products_to_discount)

def run_outlet_archiver():
    print('\n----- ℹ️  Deleting and moving sold products to archived -----\n')
    out_archiver = OutletArchiver()
    out_archiver.connect()
    products_sold_to_archive = out_archiver.select_sold_products()
    out_archiver.archive_sold_products(products_sold_to_archive)

def run_outlet_attributer():
    print('\n----- ℹ️  Updating outlet attributes -----\n')
    out_attribute_manager = OutletAttributeManager()
    out_attribute_manager.connect()
    out_attribute_manager.update_attribute_groups()
    out_attribute_manager.update_main_products_attributes()

def run_outlet_manager():
    run_outlet_creator()
    run_outlet_empty_checker()
    run_outlet_discounter()
    run_outlet_archiver()
    run_outlet_attributer()