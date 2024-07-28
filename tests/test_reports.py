import datetime
import pytest
from src.reports import spending_by_weekday, spending_by_category, spending_by_workday

from unittest.mock import patch
import pandas


@patch("pandas.DataFrame")
def test_spending_by_weekday(mock_df, operations_excel_file_dataframe, operations_excel_file_result):

    mock_df.return_value = operations_excel_file_result

    assert spending_by_weekday('01.12.2021', operations_excel_file_dataframe) == pandas.DataFrame()


@patch("pandas.DataFrame")
def test_spending_by_category(mock_df, operations_excel_file_dataframe, operations_excel_file_result):

    mock_df.return_value = operations_excel_file_result

    assert spending_by_category('Фастфуд',
                                operations_excel_file_dataframe,
                                '01.12.2021') == pandas.DataFrame()


@patch("pandas.DataFrame")
def test_spending_by_workday(mock_df, operations_excel_file_dataframe, operations_excel_file_result):

    mock_df.return_value = operations_excel_file_result

    assert spending_by_workday('01.12.2021', operations_excel_file_dataframe) == pandas.DataFrame()
