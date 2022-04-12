import datetime
import enum
from dataclasses import dataclass, field, asdict


class SaleType(int, enum.Enum):
    """ENUM to represent different ColesItem sale types"""
    NORMAL = 0
    EVERYDAY = 1
    SPECIAL = 2
    NEW = 3


@dataclass
class ColesItem:
    """Class to represent a Coles Product Item"""
    full_name: str
    brand: str
    name: str
    size: str
    sale_type: SaleType = field(init=False)
    price: float = field(init=False)
    unit_price: str
    dollar: str = field(repr=False)
    cent: str = field(repr=False)
    link: str
    partnumber: str
    id: int

    def __post_init__(self):
        self.price = float(f"{self.dollar}{self.cent}")

        if "everyday product" in self.size:
            self.sale_type = SaleType.EVERYDAY
        elif "on special" in self.size:
            self.sale_type = SaleType.SPECIAL
        elif "new product" in self.size:
            self.sale_type = SaleType.NEW
        else:
            self.sale_type = SaleType.NORMAL

        # if "everyday" in self.size:
        # everyday product, on special, new product
        # product = none
        # everyday = everyday product
        # specials = on special
        # new = new product

    @classmethod
    def from_header(cls, header):
        """Construct the ColesItem data class from Coles Product Header

        Args:
            header (_type_): A <header> html tag which contains data for a single Coles Item 
        """

        item = cls(
            full_name=header.find('span', class_="accessibility-inline").text,
            brand=header.find('span', class_="product-brand").text,
            name=header.find('span', class_="product-name").text,
            size=header.find('span', class_="package-size").text,
            dollar=header.find('span', class_="dollar-value").text,
            cent=header.find('span', class_="cent-value").text,
            unit_price=header.find('span', class_="package-price").text,
            id=header.find("h3", class_="product-title")['data-itemid'],
            link=header.find("a", class_="product-image-link")['href'],
            partnumber=header.find("h3", class_="product-title")['data-partnumber']
        )

        return item

    def to_dict(self) -> dict:
        """Return the ColesItem as a dictionary"""
        return asdict(self)

    def normalize_for_db(self) -> dict:
        """Normalize the ColesItem to a dictionary for the database"""
        item_dict = self.to_dict()

        normalized_item = {
            "id" : item_dict['id'],
            "full_name": item_dict['full_name'],
            "brand": item_dict['brand'],
            "size": item_dict["size"],
            "link": item_dict['link'],
            "partnumber" : item_dict['partnumber'],
            "price_history": [{
                "date": datetime.datetime.utcnow(),
                "price": item_dict['price'],
                "dollar": item_dict['dollar'],
                "cent": item_dict['cent'],
                "unit_price": item_dict['unit_price'],
                "sale_type": item_dict['sale_type'],
            }]
        }

        return normalized_item