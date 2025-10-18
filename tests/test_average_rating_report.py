from src.models import Product
from src.reports.average_rating_report import AverageRatingReport


class TestAverageRatingReport:
    """Тесты для отчета среднего рейтинга."""

    def setup_method(self):
        self.report = AverageRatingReport()

    def test_generate_with_empty_list(self):
        """Тест генерации отчета из пустого списка."""
        result = self.report.generate([])
        assert result == []

    def test_generate_single_brand_single_product(self):
        """Тест одного бренда с одним продуктом."""
        products = [
            Product("iphone", "apple", 1000, 4.5),
        ]

        result = self.report.generate(products)
        expected = [("apple", 4.5)]

        assert result == expected

    def test_generate_single_brand_multiple_products(self):
        """Тест одного бренда с несколькими продуктами."""
        products = [
            Product("iphone 15", "apple", 1000, 5.0),
            Product("iphone 14", "apple", 800, 4.0),
            Product("iphone 13", "apple", 600, 4.5),
        ]

        result = self.report.generate(products)
        expected_rating = (5.0 + 4.0 + 4.5) / 3

        assert len(result) == 1
        assert result[0][0] == "apple"
        assert result[0][1] == expected_rating

    def test_generate_multiple_brands(self):
        """Тест нескольких брендов с разными рейтингами."""
        products = [
            Product("iphone", "apple", 1000, 5.0),
            Product("iphone cheap", "apple", 800, 4.0),  # avg = 4.5
            Product("galaxy", "samsung", 900, 4.8),
            Product("galaxy cheap", "samsung", 700, 4.2),  # avg = 4.5
            Product("redmi", "xiaomi", 300, 3.0),  # avg = 3.0
        ]

        result = self.report.generate(products)

        assert len(result) == 3

        assert result[0][1] == 4.5
        assert result[1][1] == 4.5
        assert result[2] == ("xiaomi", 3.0)

    def test_rating_rounding(self):
        """Тест округления среднего рейтинга."""
        products = [
            Product("p1", "brand1", 100, 4.333),
            Product("p2", "brand1", 200, 4.667),
        ]

        result = self.report.generate(products)
        assert result[0][1] == 4.5  # (4.333 + 4.667) / 2 = 4.5

    def test_report_properties(self):
        """Тест свойств отчета."""
        assert self.report.name == "average-rating"
        assert self.report.headers == ["Brand", "Average Rating"]

    def test_brands_with_same_rating_stable_order(self):
        """Тест что бренды с одинаковым рейтингом имеют стабильный порядок."""
        products = [
            Product("p1", "z_brand", 100, 4.0),
            Product("p2", "a_brand", 200, 4.0),
        ]

        result = self.report.generate(products)

        assert len(result) == 2
        assert result[0][1] == 4.0
        assert result[1][1] == 4.0
