import pytest
import tempfile
import os
from typing import List


@pytest.fixture
def sample_products_data() -> List[dict]:
    """Фикстура с тестовыми данными продуктов."""
    return [
        {"name": "iphone 15", "brand": "apple", "price": "999", "rating": "4.9"},
        {"name": "galaxy s23", "brand": "samsung", "price": "899", "rating": "4.8"},
        {"name": "redmi note", "brand": "xiaomi", "price": "299", "rating": "4.6"},
        {"name": "iphone 14", "brand": "apple", "price": "799", "rating": "4.7"},
        {"name": "galaxy flip", "brand": "samsung", "price": "999", "rating": "4.5"},
    ]


@pytest.fixture
def sample_csv_content() -> str:
    """Фикстура с содержимым CSV файла."""
    return """name,brand,price,rating
iphone 15,apple,999,4.9
galaxy s23,samsung,899,4.8
redmi note,xiaomi,299,4.6"""


@pytest.fixture
def create_test_csv(sample_csv_content: str):
    """Фикстура для создания временного CSV файла."""
    def _create_test_csv(content: str = None):
        content = content or sample_csv_content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(content)
            return f.name
    return _create_test_csv


@pytest.fixture
def cleanup_files():
    """Фикстура для очистки временных файлов после тестов."""
    files_to_cleanup = []

    def _add_file(file_path):
        files_to_cleanup.append(file_path)

    yield _add_file

    for file_path in files_to_cleanup:
        try:
            os.unlink(file_path)
        except OSError:
            pass
