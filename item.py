from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    title: str
    desc: str
    price: str
    brand: str
    category: str
    stock_status: str
    ratings: int
    images: List[str]
    specs: List[str]
