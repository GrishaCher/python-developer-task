import csv
from typing import List
from .models import Product


def read_csv_files(file_paths: List[str]) -> List[Product]:
    products = []
    for file_path in file_paths:
        products.extend(read_single_csv(file_path))
    return products


def read_single_csv(file_path: str) -> List[Product]:
    products = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                product = Product.from_dict(row)
                products.append(product)
            except Exception as e:
                raise csv.Error(f"Ошибка формата CSV в файле {file_path}: {e}")
    return products
