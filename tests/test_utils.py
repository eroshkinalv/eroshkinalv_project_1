
from src.utils import greeting

from src.utils import get_card_number, get_data_this_month, expenses_this_month_by_card, get_cashback_amount
from src.utils import get_top_five_transactions, total_expenses_in_period, get_data_in_period, expenses_by_category
from src.utils import get_transfers_and_cash, get_total_income_in_period, get_income_by_category, get_exchange_rate
from src.utils import get_stock_price, get_transactions_dict
from unittest.mock import patch
import datetime
import pandas


@patch('time.strftime')
def test_greeting_5(mock_time):

    mock_time.return_value = '5'
    assert greeting(datetime.datetime.now()) == 'Доброе утро'


@patch('time.strftime')
def test_greeting_11(mock_time):

    mock_time.return_value = '11'
    assert greeting(datetime.datetime.now()) == 'Доброе утро'


@patch('time.strftime')
def test_greeting_12(mock_time):

    mock_time.return_value = '12'
    assert greeting(datetime.datetime.now()) == 'Добрый день'


@patch('time.strftime')
def test_greeting_17(mock_time):

    mock_time.return_value = '17'
    assert greeting(datetime.datetime.now()) == 'Добрый день'


@patch('time.strftime')
def test_greeting_18(mock_time):

    mock_time.return_value = '18'
    assert greeting(datetime.datetime.now()) == 'Добрый вечер'


@patch('time.strftime')
def test_greeting_22(mock_time):

    mock_time.return_value = '22'
    assert greeting(datetime.datetime.now()) == 'Добрый вечер'


@patch('time.strftime')
def test_greeting_23(mock_time):

    mock_time.return_value = '23'
    assert greeting(datetime.datetime.now()) == 'Доброй ночи'


@patch('time.strftime')
def test_greeting_(mock_time):

    mock_time.return_value = '4'
    assert greeting(datetime.datetime.now()) == 'Доброй ночи'


@patch("pandas.read_excel")
def test_get_card_number(mock_excel, operations_excel_file_path):
    mock_excel.return_value = {'Номер карты': ['*1112', '*4556']}
    assert get_card_number(operations_excel_file_path) == ['1112', '4556']


@patch("pandas.read_excel")
def test_expenses_this_month_by_card(mock_excel,
                                     operations_excel_file_content,
                                     operations_excel_file_path,
                                     current_date_and_time):

    mock_excel.return_value = operations_excel_file_content

    assert expenses_this_month_by_card(current_date_and_time, ['1112']) == {'1112': 0.0}
    assert expenses_this_month_by_card(current_date_and_time, ['5091']) == {'5091': 1.07}



@patch("pandas.read_excel")
def test_get_cashback_amount(mock_excel,
                             operations_excel_file_content,
                             operations_excel_file_path,
                             current_date_and_time):

    mock_excel.return_value = operations_excel_file_content

    assert get_cashback_amount(current_date_and_time, ['1112']) == {'1112': 0.0}
    assert get_cashback_amount(current_date_and_time, ['5091']) == {'5091': 0.01}


@patch("pandas.read_excel")
def test_get_top_five_transactions(mock_excel,
                                   operations_excel_file_content,
                                   operations_excel_file_path,
                                   current_date_and_time,
                                   top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert get_top_five_transactions(current_date_and_time) == top_five_transactions


@patch("pandas.read_excel")
def test_total_expenses_in_period(mock_excel,
                                  operations_excel_file_content,
                                  operations_excel_file_path,
                                  current_date_and_time,
                                  top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert total_expenses_in_period(current_date_and_time, 'W') == {'total_amount': 100}


@patch("pandas.read_excel")
def test_expenses_by_category(mock_excel,
                              operations_excel_file_content,
                              operations_excel_file_path,
                              current_date_and_time,
                              top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert expenses_by_category(current_date_and_time, 'W') == [{'category': 'Супермаркеты', 'amount': 99},
                                                                {'category': 'Каршеринг', 'amount': 1},
                                                                {'Остальное': 0}]


@patch("pandas.read_excel")
def test_get_transfers_and_cash(mock_excel,
                                operations_excel_file_content,
                                operations_excel_file_path,
                                current_date_and_time,
                                top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert get_transfers_and_cash(current_date_and_time, 'W') == [{'category': 'Переводы', 'amount': 0},
                                                                  {'category': 'Наличные', 'amount': 0}]


@patch("pandas.read_excel")
def test_get_total_income_in_period(mock_excel,
                                    operations_excel_file_content,
                                    operations_excel_file_path,
                                    current_date_and_time,
                                    top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert get_total_income_in_period(current_date_and_time, 'W') == {'total_amount': 0}


@patch("pandas.read_excel")
def test_get_income_by_category(mock_excel,
                                operations_excel_file_content,
                                operations_excel_file_path,
                                current_date_and_time,
                                top_five_transactions):

    mock_excel.return_value = operations_excel_file_content

    assert get_income_by_category(current_date_and_time, 'W') == []


@patch("json.loads")
def test_get_exchange_rate(mock_loads,
                           external_api_return):

    mock_loads.return_value = external_api_return

    assert get_exchange_rate(["USD"]) == {'USD': 148.97}


@patch("json.loads")
def test_get_stock_price(mock_loads, external_api_stock):

    mock_loads.return_value = external_api_stock
    current_date_and_time = datetime.datetime.strptime('2024-07-27 03:55:00', '%Y-%m-%d %H:%M:%S')
    assert get_stock_price(current_date_and_time, ['IBM']) == {'stock': 'IBM', 'price': 192.0}

