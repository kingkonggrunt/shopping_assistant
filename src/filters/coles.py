"""ColesFilters
Collection of SoupStrainer Objects to filter out a Page Source for Coles items

Example:
    from filters import ColesFilters
    soup = BeautifulSoup(page_source, 'html.parser',
            parse_only=ColesFilter.Product())
"""

import re
from bs4 import SoupStrainer

class AllProducts(SoupStrainer):
    """Filter for all products on the page"""
    def __init__(self, name="div", class_=re.compile('^product')):
        super().__init__(name, class_=class_)


class Product(SoupStrainer):
    """Filter for products with no specific tag"""
    def __init__(self, name="div", class_="product"):
        super().__init__(name, class_=class_)


class EveryDay(SoupStrainer):
    """Filter for products with an everyday product tag"""
    def __init__(self, name="div", class_="product product-every-day"):
        super().__init__(name, class_=class_)


class Specials(SoupStrainer):
    """Filter for products with a special product tag"""
    def __init__(self, name="div", class_="product product-specials"):
        super().__init__(name, class_=class_)


class MerchAssociated(SoupStrainer):
    """Filter for products with a MerchAssociated product tag"""
    def __init__(self, name="div", class_="product has-merch-assoc product-every-day"):
        super().__init__(name, class_=class_)


class New(SoupStrainer):
    """Filter for products with a New product tag"""
    def __init__(self, name="div", class_="product has-flag product-new"):
        super().__init__(name, class_=class_)


class DownDown(SoupStrainer):
    """Filter for products with a DownDown product tag"""
    def __init__(self, name="div", class_="product product-down-down"):
        super().__init__(name, class_=class_)
