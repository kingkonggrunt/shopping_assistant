from dataclasses import dataclass, field, asdict
import enum


class SaleType(int, enum.Enum):
    normal = 0
    everyday = 1
    special = 2
    new = 3


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
            self.sale_type = SaleType.everyday
        elif "on special" in self.size:
            self.sale_type = SaleType.special
        elif "new product" in self.size:
            self.sale_type = SaleType.new
        else:
            self.sale_type = SaleType.normal
        
        # if "everyday" in self.size:
        # everyday product, on special, new product
        # product = none
        # everyday = everyday product
        # specials = on special
        # new = new product
        
    def to_dict(self):
        return asdict(self)
            