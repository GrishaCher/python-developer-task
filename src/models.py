from dataclasses import dataclass


@dataclass
class Product:
    name: str
    brand: str
    price: float
    rating: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        return cls(
            name=data['name'],
            brand=data['brand'],
            price=float(data['price']),
            rating=float(data['rating'])
        )
