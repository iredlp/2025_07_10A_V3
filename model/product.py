from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Product:
    product_id: int
    product_name: str
    brand_id: int
    category_id: int
    model_year: int
    list_price: float

  #  oldest_driver_dob:Optional[int] = None  #valore opzionale

    list_prodotti:  list = field(default_factory=list)
    #popolarita: set = field(default_factory=set)
    num_vendite: int = 0

    def __hash__(self):
        return hash(self.product_id)

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.product_id == other. product_id
        return False

    def __repr__(self):
        return (f"{self.product_name} ({self. product_id}) ")
                # if self.year is not None else 'N/D'})")