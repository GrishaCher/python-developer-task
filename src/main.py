import argparse
from tabulate import tabulate
from .file_reader import read_csv_files
from .reports import get_report


def main():
    parser = argparse.ArgumentParser(description='Генератор отчетов из CSV файлов')
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам'
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Название отчета'
    )

    args = parser.parse_args()

    try:
        validate_files(args.files)

        products = read_csv_files(args.files)
        if products == []:
            raise ValueError("Нет данных")
        report = get_report(args.report)
        report_data = report.generate(products)

        print(f"Отчет: {report.name}")
        print(tabulate(report_data, headers=report.headers, tablefmt="grid"))

    except Exception as e:
        print(f"Ошибка: {e}")


def validate_files(file_paths):
    for file_path in file_paths:
        if not file_path.lower().endswith('.csv'):
            raise ValueError(f"Файл '{file_path}' должен иметь расширение .csv")
        try:
            with open(file_path, 'r'):
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{file_path}' не существует")
        except IOError as e:
            raise ValueError(f"Не удается прочитать файл '{file_path}': {e}")


if __name__ == "__main__":
    main()
