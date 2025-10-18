# python-developer-task

## Быстрая установка и запуск


```bash
# Клонирование репозитория
git clone https://github.com/GrishaCher/python-developer-task
cd python-developer-task

# Установка зависимостей
pip install .

# Запуск
python -m src.main --files path-to-file1 path-to-file2 ... --report average-rating
```

## Пример работы

```bash
python -m src.main --files "test-data/products1.csv" --report average-rating
```
<img width="300" height="220" alt="image" src="https://github.com/user-attachments/assets/54ecd27e-0b84-42ed-9f10-14c1ec3cd874" />

```bash
python -m src.main --files "test-data/products1.csv" "test-data/products2.csv" --report average-rating
```
<img width="300" height="220" alt="image" src="https://github.com/user-attachments/assets/4b742158-b8a5-4226-b023-c2eb7fd94542" />

```bash
python -m src.main --files "test-data/non-exist-file.csv" --report average-rating
```
<img width="800" height="40" alt="image" src="https://github.com/user-attachments/assets/554a3223-6991-4036-bfa5-88a25856910e" />

```bash
python -m src.main --files  --report average-rating
```
<img width="800" height="80" alt="image" src="https://github.com/user-attachments/assets/77cae667-8f95-4e00-a2e2-8c8501794b2a" />

```bash
ython -m src.main --files "test-data/products1.csv" "test-data/products2.csv" --report wrong-report
```
<img width="750" height="80" alt="image" src="https://github.com/user-attachments/assets/79eb877a-39f2-4e22-9bd7-a66a17b49fe5" />

## Добавление отчётов

Создать класс отчёта унаследовав его от BaseReport и реализовать все его методы и атрибуты.

Добавить новый отчет в реестр отчетов src/reports/init.py в REPORTS
