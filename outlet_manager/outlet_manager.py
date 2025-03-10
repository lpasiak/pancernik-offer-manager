from .models.outlet_product import OutletProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts, ShoperPictures
import config

shoper_client = ShoperAPIClient(
    site_url=config.SHOPER_SITE_URL,
    login=config.SHOPER_LOGIN,
    password=config.SHOPER_PASSWORD
)
shoper_client.connect()
shoper_products = ShoperProducts(shoper_client)
shoper_pictures = ShoperPictures(shoper_client)
outlets_to_create = [
    {
        'outlet_code': 'OUT_XD1',
        'damage_type': 'USZ',
        'product_id': 86918
    }
    # {
    #     'outlet_code': 'OUT_XD2',
    #     'damage_type': 'USZ',
    #     'product_id': 10742
    # },    
    # {
    #     'outlet_code': 'OUT_XD3',
    #     'damage_type': 'USZ',
    #     'product_id': 10743
    # }
]

def create_outlet_offers(outlet_data=outlets_to_create):
    for product in outlets_to_create:
        # Get source product data
        source_product = shoper_products.get_a_product_by_code(product['product_id'], pictures=True)
        
        new_outlet = OutletProduct(source_product, product['outlet_code'], product['damage_type'])

        # Create outlet offer
        try:
            product_data = new_outlet.transform_to_outlet()
            created_offer_id = shoper_products.create_product(product_data)
            
            if not created_offer_id:
                print(f"❌ No product ID in response for {product['product_id']}")
                continue
                
            print(f"✅ Created outlet product with ID: {created_offer_id}")
            
            # Update source product barcode
            shoper_products.update_product(created_offer_id, barcode=new_outlet.barcode)

            # Update related products
            shoper_products.update_product(created_offer_id, related=new_outlet.related)

            # Update url
            product_url_json = {'pl_PL': { 'seo_url': new_outlet.product_url(created_offer_id)}}
            response = shoper_products.update_product(created_offer_id, translations=product_url_json)

            # Update images
            outlet_pictures = new_outlet.set_outlet_pictures(created_offer_id)

            for picture in outlet_pictures:
                response = shoper_pictures.update_product_image(created_offer_id, picture)
    
            # Update stock.fx_id to the main image
            created_product = shoper_products.get_a_product_by_code(created_offer_id)
            stock_gfx = created_product['main_image']['gfx_id']
            stock_gfx_id = {'gfx_id': stock_gfx}
            shoper_products.update_product(created_offer_id, stock=stock_gfx_id)


            print('-----------------------------------')
        except Exception as e:
            print(f'❌ Error creating outlet offer for product {product["product_id"]}: {e}')
