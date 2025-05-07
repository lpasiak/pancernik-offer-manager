from outlet_manager.managers.outlet_creator import OutletCreator
from outlet_manager.managers.outlet_attributes import OutletAttributeManager
from outlet_manager.managers.outlet_lacking import OutletLackingManager
from outlet_manager.managers.outlet_discount import OutletDiscountManager
from outlet_manager.managers.outlet_archiver import OutletArchiver

def run_outlet_manager():
    """Run all functions related to outlets (Creation, Discounts, Deletion...)"""

    print('----- ℹ️ Creating outlet offers -----')
    out_creator = OutletCreator()
    out_creator.connect()
    products_to_publish = out_creator.get_offers_ready_to_publish()
    out_creator.create_outlet_offers(products_to_publish)

    print('----- ℹ️ Checking for offers not found on Shoper -----')
    out_lacking_products_manager = OutletLackingManager()
    out_lacking_products_manager.connect()
    out_lacking_products_manager.move_products_to_lacking()

    print('----- ℹ️ Setting outlet discounts -----')
    out_discount_manager = OutletDiscountManager()
    out_discount_manager.connect()
    products_to_discount = out_discount_manager.select_products_to_discount()
    out_discount_manager.create_discounts(products_to_discount)

    print('----- ℹ️ Deleting and moving sold products to archived -----')
    out_archiver = OutletArchiver()
    out_archiver.connect()
    products_sold_to_archive = out_archiver.select_sold_products()
    out_archiver.archive_sold_products(products_sold_to_archive)

    print('----- ℹ️ Updating outlet attributes -----')
    out_attribute_manager = OutletAttributeManager()
    out_attribute_manager.connect()
    out_attribute_manager.update_attribute_groups()
    out_attribute_manager.update_main_products_attributes()