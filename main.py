from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.attributes import ShoperAttributes
from connections.shoper.categories import ShoperCategories
import config
import pandas as pd

client = ShoperAPIClient(
    site_url=config.SHOPER_SITE_URL,
    login=config.SHOPER_LOGIN,
    password=config.SHOPER_PASSWORD
)
client.connect()

shoper_products = ShoperProducts(client)
shoper_attributes = ShoperAttributes(client)
shoper_categories = ShoperCategories(client)

# shoper_products.get_all_products()

x = shoper_attributes.get_all_attribute_groups()
print(x)
y = shoper_attributes.get_all_attributes()
print(y)
