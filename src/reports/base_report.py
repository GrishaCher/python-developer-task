from abc import ABC, abstractmethod
from typing import List
from ..models import Product


class BaseReport(ABC):

    @abstractmethod
    def generate(self, products: List[Product]) -> List[tuple]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def headers(self) -> List[str]:
        pass
