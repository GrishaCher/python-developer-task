from typing import List, Tuple
from collections import defaultdict
from ..models import Product
from .base_report import BaseReport


class AverageRatingReport(BaseReport):

    def generate(self, products: List[Product]) -> List[Tuple[str, float]]:
        brand_ratings = defaultdict(list)

        for product in products:
            brand_ratings[product.brand].append(product.rating)

        average_ratings = []
        for brand, ratings in brand_ratings.items():
            avg_rating = sum(ratings) / len(ratings)
            average_ratings.append((brand, round(avg_rating, 2)))

        average_ratings.sort(key=lambda x: x[1], reverse=True)

        return average_ratings

    @property
    def name(self) -> str:
        return "average-rating"

    @property
    def headers(self) -> List[str]:
        return ["Brand", "Average Rating"]
