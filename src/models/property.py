from dataclasses import dataclass


@dataclass
class Property:
    address: str
    price: int
    bedrooms: int
    bathrooms: int
    size: int
