from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
import config

client = ShoperAPIClient(
    site_url=config.SHOPER_SITE_URL,
    login=config.SHOPER_LOGIN,
    password=config.SHOPER_PASSWORD
)
client.connect()

shoper_products = ShoperProducts(client)
# shoper_products.get_all_products()

