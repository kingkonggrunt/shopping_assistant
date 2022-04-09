from dataclasses import dataclass, field

@dataclass
class ColesItem:
    """Class to represent a Coles Product Item"""
    full_name: str
    brand: str
    name: str
    size: str
    price: float = field(init=False)
    unit_price: str
    dollar: str = field(repr=False)
    cent: str = field(repr=False)
    link: str
    partnumber: str
    id: int
    
    def __post_init__(self):
        self.price = float(f"{self.dollar}{self.cent}")