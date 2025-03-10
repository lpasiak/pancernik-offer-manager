import os, random
import config

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
        self.outlet_code = outlet_code
        self.damage_type = damage_type
        self.description = self._create_description()
        self.product_description_short = config.outlet_info.damage_types_short[self.damage_type]
        self.price = self._set_outlet_price()
        self.product_type = self._set_product_type()
        self.tags = [6] if config.SITE == 'MAIN' else [1]
        self.category_list = self._set_category_list()
        self.main_category_id = self.source_product['category_id']

    def transform_to_outlet(self):
        """Transform the product to an outlet product."""
        return self
    
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

    def _set_product_type(self):
        """Set the product type based on the source product attributes."""
        if self.source_product['attributes'] != []:
            try:
                if config.SITE == 'MAIN':
                    return self.source_product['attributes']['550']['1370']
                elif config.SITE == 'TEST':
                    return self.source_product['attributes']['8']['28']
                else:
                    raise ValueError(f"Unknown site configuration: {config.SITE}")
                
            except (KeyError, TypeError):
                print(f"Warning: Could not determine product type for {self.outlet_code}")
                return None
        return None

    def _create_description(self):
        """Create the description for the outlet product by merging the outlet description and the source description."""
        outlet_description = config.outlet_info.damage_types_long[self.damage_type].replace('[SKU_OUTLET_CODE]', self.outlet_code)
        source_description = self.source_product["translations"]["pl_PL"]["description"]
        
        return outlet_description + source_description

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

        return float(price) * config.OUTLET_DISCOUNT_PERCENTAGE
    
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

    def product_url(self, product_id):
        """Generate the product URL based on the source product and new outlet product ID."""
        product_url = self.source_product['translations']['pl_PL'].get('seo_url', '')

        return product_url + f'-{product_id}'