import pytest
import csv
from unittest.mock import patch, MagicMock, call


class TestMain:
    """Тесты для основного скрипта main.py."""

    @patch('src.main.read_csv_files')
    @patch('src.main.get_report')
    @patch('src.main.tabulate')
    def test_main_successful_execution(
        self,
        mock_tabulate,
        mock_get_report,
        mock_read_csv
    ):
        """Тест успешного выполнения main скрипта."""
        mock_products = [MagicMock()]
        mock_read_csv.return_value = mock_products

        mock_report = MagicMock()
        mock_report.name = "average-rating"
        mock_report.headers = ["Brand", "Average Rating"]
        mock_report.generate.return_value = [("apple", 4.5), ("samsung", 4.3)]
        mock_get_report.return_value = mock_report

        mock_tabulate.return_value = "mocked table output"

        test_args = ["main.py", "--files", "test.csv", "--report", "average-rating"]

        with patch('sys.argv', test_args):
            with patch('src.main.validate_files'):
                with patch('builtins.print') as mock_print:
                    from src.main import main
                    main()

                    mock_read_csv.assert_called_once_with(["test.csv"])
                    mock_get_report.assert_called_once_with("average-rating")
                    mock_report.generate.assert_called_once_with(mock_products)
                    mock_tabulate.assert_called_once_with(
                        [("apple", 4.5), ("samsung", 4.3)],
                        headers=["Brand", "Average Rating"],
                        tablefmt="grid"
                    )

                    expected_calls = [
                        call("Отчет: average-rating"),
                        call("mocked table output")
                    ]
                    mock_print.assert_has_calls(expected_calls)

    def test_main_missing_arguments(self):
        """Тест что отсутствие обязательных аргументов вызывает ошибку."""
        test_args = ["main.py"]

        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                from src.main import main
                main()

    def test_main_missing_files_argument(self):
        """Тест что отсутствие --files вызывает ошибку."""
        test_args = ["main.py", "--report", "average-rating"]

        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                from src.main import main
                main()

    def test_main_missing_report_argument(self):
        """Тест что отсутствие --report вызывает ошибку."""
        test_args = ["main.py", "--files", "test.csv"]

        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                from src.main import main
                main()

    def test_main_file_validation_extension_error(self):
        """Тест валидации файлов с не-CSV расширением."""
        test_args = ["main.py", "--files", "test.txt", "--report", "average-rating"]

        with patch('sys.argv', test_args):
            with patch('builtins.print') as mock_print:
                from src.main import main
                main()

                mock_print.assert_called_once()
                call_args = mock_print.call_args[0][0]
                assert "должен иметь расширение .csv" in call_args

    def test_main_file_not_found_error(self):
        """Тест когда файл не существует."""
        test_args = ["main.py", "--files", "nonexistent.csv", "--report", "average-rating"]  # noqa: E501

        with patch('sys.argv', test_args):
            with patch('builtins.print') as mock_print:
                from src.main import main
                main()

                mock_print.assert_called_once()
                call_args = mock_print.call_args[0][0]
                assert "не существует" in call_args

    @patch('src.main.read_csv_files')
    def test_main_invalid_report_name(self, mock_read_csv):
        """Тест что неверное имя отчета вызывает ошибку."""
        mock_read_csv.return_value = [MagicMock()]

        test_args = ["main.py", "--files", "test.csv", "--report", "invalid-report"]

        with patch('sys.argv', test_args):
            with patch('src.main.validate_files'):
                with patch('builtins.print') as mock_print:
                    from src.main import main
                    main()

                    mock_print.assert_called_once()
                    call_args = mock_print.call_args[0][0]
                    assert "Отчет 'invalid-report' не найден" in call_args

    @patch('src.main.read_csv_files')
    @patch('src.main.get_report')
    @patch('src.main.tabulate')
    def test_main_no_data(self, mock_tabulate, mock_get_report, mock_read_csv):
        """Тест когда нет данных для отчета."""
        mock_read_csv.return_value = []

        test_args = ["main.py", "--files", "test.csv", "--report", "average-rating"]

        with patch('sys.argv', test_args):
            with patch('src.main.validate_files'):
                with patch('builtins.print') as mock_print:
                    from src.main import main
                    main()

                    mock_print.assert_any_call("Ошибка: Нет данных")

                    mock_get_report.assert_not_called()
                    mock_tabulate.assert_not_called()

    def test_main_csv_parsing_error(self):
        """Тест ошибки парсинга CSV."""
        with patch('src.main.read_csv_files') as mock_read_csv:
            mock_read_csv.side_effect = csv.Error("Ошибка формата CSV в файле test.csv: 'name'")  # noqa: E501

            test_args = ["main.py", "--files", "test.csv", "--report", "average-rating"]

            with patch('sys.argv', test_args):
                with patch('src.main.validate_files'):
                    with patch('builtins.print') as mock_print:
                        from src.main import main
                        main()

                        mock_print.assert_called_once_with("Ошибка: Ошибка формата CSV в файле test.csv: 'name'")  # noqa: E501

    def test_main_multiple_files_success(self):
        """Тест успешной обработки нескольких файлов."""
        with patch('src.main.read_csv_files') as mock_read_csv:
            mock_read_csv.return_value = [MagicMock()]

            with patch('src.main.get_report') as mock_get_report:
                mock_report = MagicMock()
                mock_report.name = "average-rating"
                mock_report.headers = ["Brand", "Rating"]
                mock_report.generate.return_value = [("apple", 4.5)]
                mock_get_report.return_value = mock_report

                with patch('src.main.tabulate') as mock_tabulate:
                    mock_tabulate.return_value = "table"

                    test_args = [
                        "main.py",
                        "--files",
                        "file1.csv",
                        "file2.csv",
                        "file3.csv",
                        "--report",
                        "average-rating"
                    ]

                    with patch('sys.argv', test_args):
                        with patch('src.main.validate_files'):
                            with patch('builtins.print'):
                                from src.main import main
                                main()

                                mock_read_csv.assert_called_once_with(
                                    [
                                        "file1.csv",
                                        "file2.csv",
                                        "file3.csv"
                                    ]
                                )

    def test_validate_files_function_invalid_extension(self):
        """Тест функции валидации файлов с не-CSV расширением."""
        from src.main import validate_files

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            with pytest.raises(ValueError, match="должен иметь расширение .csv"):
                validate_files([f.name])

    def test_validate_files_function_nonexistent_file(self):
        """Тест функции валидации несуществующего файла."""
        from src.main import validate_files

        with pytest.raises(FileNotFoundError):
            validate_files(["nonexistent_file.csv"])
