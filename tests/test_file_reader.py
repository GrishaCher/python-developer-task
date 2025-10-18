import pytest
import csv
from src.file_reader import read_csv_files, read_single_csv
from src.models import Product


class TestFileReader:
    """Тесты для модуля чтения CSV файлов."""

    def test_read_single_csv_valid_data(self, create_test_csv, cleanup_files):
        """Тест чтения корректного CSV файла."""
        file_path = create_test_csv()
        cleanup_files(file_path)

        products = read_single_csv(file_path)

        assert len(products) == 3
        assert isinstance(products[0], Product)
        assert products[0].name == "iphone 15"
        assert products[0].brand == "apple"
        assert products[0].price == 999.0
        assert products[0].rating == 4.9

    def test_read_multiple_files(self, create_test_csv, cleanup_files):
        """Тест чтения нескольких CSV файлов."""
        content1 = """name,brand,price,rating
product1,brand1,100,4.5"""

        content2 = """name,brand,price,rating
product2,brand2,200,4.0"""

        file1 = create_test_csv(content1)
        file2 = create_test_csv(content2)
        cleanup_files(file1)
        cleanup_files(file2)

        products = read_csv_files([file1, file2])

        assert len(products) == 2
        assert products[0].brand == "brand1"
        assert products[1].brand == "brand2"

    def test_read_csv_with_invalid_data_raises_error(self, create_test_csv, cleanup_files):  # noqa: E501
        """Тест что некорректные строки вызывают ошибку (все или ничего)."""
        content = """name,brand,price,rating
valid product,apple,100,4.5
invalid product,,not_number,bad_rating
another valid,samsung,200,4.0"""

        file_path = create_test_csv(content)
        cleanup_files(file_path)

        with pytest.raises(csv.Error, match="Ошибка формата CSV"):
            read_single_csv(file_path)

    def test_read_csv_missing_columns_raises_error(self, create_test_csv, cleanup_files):  # noqa: E501
        """Тест что отсутствие обязательных колонок вызывает ошибку."""
        content = """name,price,rating
iphone,999,4.9"""

        file_path = create_test_csv(content)
        cleanup_files(file_path)

        with pytest.raises(csv.Error, match="Ошибка формата CSV"):
            read_single_csv(file_path)

    def test_read_empty_csv_returns_empty_list(self, create_test_csv, cleanup_files):
        """Тест чтения пустого CSV файла (только заголовки)."""
        content = "name,brand,price,rating"

        file_path = create_test_csv(content)
        cleanup_files(file_path)

        products = read_single_csv(file_path)
        assert products == []

    def test_read_nonexistent_file_raises_error(self):
        """Тест что несуществующий файл вызывает ошибку."""
        with pytest.raises(FileNotFoundError):
            read_single_csv("nonexistent_file.csv")

    def test_file_with_only_headers_returns_empty_list(self, create_test_csv, cleanup_files):  # noqa: E501
        """Тест файла только с заголовками."""
        content = "name,brand,price,rating"

        file_path = create_test_csv(content)
        cleanup_files(file_path)

        products = read_single_csv(file_path)
        assert products == []

    def test_multiple_files_one_invalid_raises_error(self, create_test_csv, cleanup_files):  # noqa: E501
        """Тест что если один из нескольких файлов некорректен - падает ошибка."""
        valid_content = """name,brand,price,rating
product1,brand1,100,4.5"""

        invalid_content = """name,brand,price,rating
product2,brand2,not_number,4.0"""

        valid_file = create_test_csv(valid_content)
        invalid_file = create_test_csv(invalid_content)
        cleanup_files(valid_file)
        cleanup_files(invalid_file)

        with pytest.raises(csv.Error, match="Ошибка формата CSV"):
            read_csv_files([valid_file, invalid_file])
