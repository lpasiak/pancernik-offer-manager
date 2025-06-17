import random
import config
from utils.logger import get_outlet_logger

class OutletProduct:
    """
    OutletProduct is a Class that transforms a regular product into a product that is an outlet product.
    Args:
        product_data (dict): The product data from the Shoper API.
        outlet_code (str): The outlet code.
        damage_type (str): The damage type one of the ['USZ', 'ZAR', 'OBA']
    """
    def __init__(self, product_data, outlet_code, damage_type):
        
        self._validate_input(product_data, damage_type)
        
        self.source_product = product_data
        self.source_product_id = self.source_product['product_id']
        self.barcode = self.source_product['code']
        self.outlet_code = outlet_code
        self.damage_type = damage_type
        self.product_description = self._create_description()
        self.product_description_short = config.outlet_info.damage_types_short[self.damage_type]
        self.price = self._set_outlet_price()
        self.product_type = self._set_product_type()
        self.tags = [6] if config.SITE == 'MAIN' else [1]
        self.category_list = self._set_category_list()
        self.main_category_id = self.source_product['category_id']
        self.related = self.source_product['related']
        self.attributes = self._transform_attributes()
        self.outlet_logger = get_outlet_logger().get_logger()

    def transform_to_outlet(self):
        """Transform the product to an outlet product and return as a dicitonary."""
        outlet_product = {
        'producer_id': self.source_product['producer_id'],
        'category_id': self.main_category_id,
        'categories': self.category_list,
        'code': self.outlet_code,
        'additional_producer': self.source_product.get('additional_producer', ''),
        'pkwiu': self.source_product['pkwiu'],

        'translations': {
            "pl_PL": {
                'name': f'OUTLET: {self.source_product["translations"]["pl_PL"]["name"]}',
                'short_description': self.product_description_short,
                'description': self.product_description,
                'active': '1',
                'order': random.randint(1,5)
            }
        },
        'stock': {
            'price': self.price,
            'active': 1,
            'stock': 1,
            'availability_id': None,
            'delivery_id': 1,
            'weight': 0.2,
            'weight_type': self.source_product.get('weight_type', ''),
        },
        'tax_id': self.source_product['tax_id'],
        'unit_id': self.source_product['unit_id'],
        'vol_weight': self.source_product['vol_weight'],
        'currency_id': self.source_product['currency_id'],
        'gauge_id': self.source_product['gauge_id'],
        'unit_price_calculation': self.source_product['unit_price_calculation'],
        'newproduct': False,
        'related': self.related,
        'tags': self.tags,
        'type': self.source_product['type'],
        'safety_information': self.source_product['safety_information'],
        'feeds_excludes': self.source_product['feeds_excludes'],
        'attributes': self.attributes
        }

        return outlet_product
    
    def _validate_input(self, product_data, damage_type):
        """Validate input parameters.
        Args:
            product_data (dict): The product data from the Shoper API
            damage_type (str): The damage type
        Raises:
            ValueError: If any validation fails
        """
        if damage_type not in config.OUTLET_VALID_DAMAGE_TYPES:
            raise ValueError(f"Invalid damage type: {damage_type}. Must be one of: {config.OUTLET_VALID_DAMAGE_TYPES}")

        if not isinstance(product_data, dict):
            raise ValueError("product_data must be a dictionary")
            
        # Check if product data is an error response
        if product_data.get('success') is False:
            raise ValueError(f"Invalid product data: {product_data.get('error', 'Unknown error')}")
            
        # Check for required fields
        required_fields = ['product_id', 'code', 'category_id', 'translations', 'stock']
        missing_fields = [field for field in required_fields if field not in product_data]
        if missing_fields:
            raise ValueError(f"Product data is missing required fields: {', '.join(missing_fields)}")

    def _set_product_type(self):
        """Set the product type based on the source product attributes."""
        if self.source_product['attributes'] != []:
            try:
                group_id = config.PRODUCT_TYPE[config.SITE]['group']
                type_id = config.PRODUCT_TYPE[config.SITE]['id']
                return self.source_product['attributes'][group_id][type_id]
                
            except (KeyError, TypeError):
                self.outlet_logger.warning(f'⚠️ Warning: Could not determine product type for {self.outlet_code}')
                return None
        return None

    def _create_description(self):
        """Create the description for the outlet product by merging the outlet description and the source description."""
        outlet_description = config.outlet_info.damage_types_long[self.damage_type].replace('[SKU_OUTLET_CODE]', self.outlet_code)
        source_description = self.source_product["translations"]["pl_PL"]["description"]
        description = outlet_description + source_description
        
        # Remove formulas from description
        for formula in config.outlet_info.formulas_to_remove.values():
            if formula in description:
                description = description.replace(formula, '')
        
        return description

    def _set_outlet_price(self):
        """
        Calculate the outlet price.
        Returns:
            float: The calculated outlet price (80% of original price)
        """
        if self.source_product['promo_price']:
            price = self.source_product['promo_price']
        else:
            price = self.source_product['stock']['price']

        return float(price) - float(price) * (config.OUTLET_DISCOUNT_PERCENTAGE / 100)
    
    def _set_category_list(self):
        """Get the category list from the source product and append the correct outlet category.
        Returns:
            list: List of categories including the outlet category
        """
        categories = self.source_product['categories']
        outlet_category = self._get_outlet_category()
        return categories + [outlet_category]

    def _get_outlet_category(self):
        """Determine the outlet category based on site and product type.
        Returns:
            int: The outlet category ID
        """
        if config.SITE == 'TEST':
            return 1322

        # Main site category logic
        if self.product_type is None:
            return 7525  # Default category

        product_type = self.product_type.lower()
        
        # Category mapping for main site
        category_mapping = {
            'słuchawki': 7611,
            'pasek do smartwatcha': 7612,
            'adapter': 7547,
            'ładowarka sieciowa': 7537,
            'ładowarka samochodowa': 7538,
            'ładowarka indukcyjna': 7539,
            'powerbank': 7541,
            'kabel': 7542,
            'listwa zasilająca': 7543,
            'rysik': 7544,
            'obiektyw do telefonu': 7545,
            'akcesoria rowerowe': 7546,
            'selfie-stick': 7548
        }

        # Try to get category from mapping
        outlet_category = category_mapping.get(product_type)
        if outlet_category:
            return outlet_category

        # Special case for phone holders
        if "uchwyt" in product_type and "telefon" in product_type:
            return 7540

        # Default category if no matches found
        return 7525

    def _transform_attributes(self):
        """Transform the attributes of the source product to the attributes of the outlet product."""

        src_product_attribute_dict = self.source_product['attributes']
        attribute_dict = {}

        # If attributes is an empty list, just return empty dict with outlet attributes
        if not src_product_attribute_dict:  # This works for empty list/dict
            if config.SITE == 'MAIN':
                attribute_dict['1402'] = ''     # _outlet
                attribute_dict['1538'] = 'Tak'  # Outlet
            return attribute_dict

        # Handle if attributes is a list
        if isinstance(src_product_attribute_dict, list):
            for attribute in src_product_attribute_dict:
                if isinstance(attribute, dict):
                    for key, value in attribute.items():
                        attribute_dict[key] = value
                else:
                    pass
                        
        # Handle if attributes is a dictionary
        elif isinstance(src_product_attribute_dict, dict):
            for group, attributes in src_product_attribute_dict.items():
                if isinstance(attributes, dict):
                    for key, value in attributes.items():
                        attribute_dict[key] = value
                else:
                    pass

        # Add outlet attributes
        if config.SITE == 'MAIN':
            attribute_dict['1402'] = ''     # _outlet
            attribute_dict['1538'] = 'Tak'  # Outlet

        return attribute_dict
    
    def set_outlet_pictures(self, new_product_id):
        if not self.source_product.get('img'):
            return []
        
        source_images = self.source_product['img']
        final_images = []
        site_url = config.SHOPER_SITE_URL
        
        for image in source_images:
            image_id = f"{image['unic_name']}.{image['extension']}"

            image_item = {
                'product_id': new_product_id,
                'url': f"{site_url}/userdata/public/gfx/{image_id}",
                'main': str(image['main']),
                'order': image['order'],
                'name': image['translations']['pl_PL']['name']
            }
            final_images.append(image_item)

        final_images.sort(key=lambda x: x['order'])

        return final_images

    def product_url(self, product_id):
        """Generate the product URL based on the source product and new outlet product ID."""
        product_url = self.source_product['translations']['pl_PL'].get('seo_url', '')

        return f'{product_url}-outlet-{product_id}'
