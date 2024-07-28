import datetime
import pytest
from src.services import cashback_offers, investment_bank, simple_search, search_by_phone_numbers, search_transfers
import json
from unittest.mock import patch, Mock
import pandas


@patch("pandas.DataFrame")
def test_cashback_offers(mock_df, operations_excel_file_dataframe):

    mock_df.return_value = operations_excel_file_dataframe

    assert cashback_offers('2021', '12', operations_excel_file_dataframe) == '{}'


@patch("pandas.DataFrame")
def test_investment_bank(mock_df, operations_excel_file_dataframe):

    mock_df.return_value = operations_excel_file_dataframe

    assert investment_bank('12', '10', [{'2021-11-01': -95.0}, {'2021-11-01': -103.0}]) == 0


def test_simple_search(json_fastfood_result):

    assert simple_search('Владимир') == json_fastfood_result


def test_search_by_phone_numbers(json_phone_result):

    assert search_by_phone_numbers('+7 962 717-08-52') == json_phone_result
