from unittest.mock import patch

from src.services import cashback_offers, investment_bank


@patch("pandas.DataFrame")
def test_cashback_offers(mock_df, operations_excel_file_dataframe):

    mock_df.return_value = operations_excel_file_dataframe

    assert cashback_offers('2021', '12', operations_excel_file_dataframe) == '{}'


@patch("pandas.DataFrame")
def test_investment_bank(mock_df, operations_excel_file_dataframe):

    mock_df.return_value = operations_excel_file_dataframe

    assert investment_bank('12', '10', [{'2021-11-01': -95.0}, {'2021-11-01': -103.0}]) == 0
