from .average_rating_report import AverageRatingReport
from typing import Union


REPORTS = {
    "average-rating": AverageRatingReport
}


def get_report(report_name: str) -> Union[AverageRatingReport]:
    if report_name not in REPORTS:
        raise ValueError(f'''Отчет '{report_name}' не найден.
Доступные: {list(REPORTS.keys())}''')
    return REPORTS[report_name]()
