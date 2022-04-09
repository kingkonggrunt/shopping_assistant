from bs4 import SoupStrainer



class Product(SoupStrainer):
    def __init__(self, name="div", class_="product"):
        super().__init__(name, class_=class_)


class EveryDay(SoupStrainer):
    def __init__(self, name="div", class_="product product-every-day"):
        super().__init__(name, class_=class_)

        
class Specials(SoupStrainer):
    def __init__(self, name="div", class_="product product-specials"):
        super().__init__(name, class_=class_)

        
class MerchAssociated(SoupStrainer):
    def __init__(self, name="div", class_="product has-merch-assoc product-every-day"):
        super().__init__(name, class_=class_)

        
class New(SoupStrainer):
    def __init__(self, name="div", class_="product has-flag product-new"):
        super().__init__(name, class_=class_)

        
class DownDown(SoupStrainer):
    def __init__(self, name="div", class_="product-down-down"):
        super().__init__(name, class_=class_)
