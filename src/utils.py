import datetime
import json
import os
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

op_xlsx = os.path.abspath(r'../data/operations.xlsx')

# op_xlsx = r'C:\Users\liudo\PycharmProjects\skypro_project_1\data\operations.xlsx'

load_dotenv(r"../.env")
currency_exchange_api = os.getenv('CURRENCY_EXCHANGE_API_KEY')
st_api = os.getenv('STOCK_PRICES_API_KEY')

with open(r'../user_settings.json', 'r', encoding='utf-8') as file:
    user_settings = json.load(file)


def greeting(time: datetime.datetime) -> str:
    """Возвращает приветствие в зависимости от текущего времени"""

    current_hour = int(time.strftime('%H'))

    if 5 <= current_hour < 12:
        personal_greeting = 'Доброе утро'

    elif 12 <= current_hour < 18:
        personal_greeting = 'Добрый день'

    elif 18 <= current_hour < 23:
        personal_greeting = 'Добрый вечер'

    elif 0 <= current_hour < 5 or current_hour == 23:
        personal_greeting = 'Доброй ночи'

    return personal_greeting


def get_card_number(xlsx_file: str = op_xlsx) -> List:
    """Возвращает последние четыре цифры номеров карт."""

    excel_data = pd.read_excel(xlsx_file)
    card_numbers_masked = list(set(excel_data['Номер карты']))
    card_numbers = sorted([str(num)[-4:] for num in card_numbers_masked if str(num) != 'nan'])

    return card_numbers


def get_data_this_month(current_date: datetime.datetime, xlsx_file: str = op_xlsx) -> pd.DataFrame:
    """Возвращает DataFrame с данными о банковских операциях
    за период с первого числа текущего месяца по текущее число."""

    try:
        excel_data = pd.read_excel(xlsx_file)
        current_month = current_date.strftime('%m.%Y')

    except FileNotFoundError:
        tr_this_month = pd.DataFrame({})

    except AttributeError:
        tr_this_month = pd.DataFrame({})

    else:
        # Даты всех операций:
        tr_dates = list(excel_data['Дата операции'])
        # Даты операций в текущий период:
        tr_dates_current_month = [d for d in tr_dates if current_month in d]
        # Операции в текущий период:
        tr_this_month = excel_data.loc[excel_data['Дата операции'].isin(tr_dates_current_month)]

    return tr_this_month


def expenses_this_month_by_card(cur_date: datetime.datetime, card_num: List, xl_file: str = op_xlsx) -> Dict[Any, Any]:
    """Возвращает общую сумму расходов по каждой карте за период с первого числа текущего месяца по текущее число."""

    tr_this_month = get_data_this_month(cur_date, xl_file)

    if not list(tr_this_month):
        cards_spending_info = dict()

    else:
        cards_spending_info = {}
        for card in card_num:
            info_by_card = tr_this_month.loc[tr_this_month['Номер карты'] == '*' + card]
            spending_by_card = abs(sum([sp for sp in list(info_by_card['Сумма платежа']) if sp < 0]))
            cards_spending_info[card] = round(float(spending_by_card), 2)

    return cards_spending_info


def get_cashback_amount(current_date: datetime.datetime, card_numbers: List, xlsx_file: str = op_xlsx) -> Dict:
    """Возвращает кешбэк (1 рубль на каждые 100 рублей) для каждой карты
        за период с первого числа текущего месяца по текущее число."""

    tr_this_month = get_data_this_month(current_date, xlsx_file)

    if not list(tr_this_month):
        cards_cashback_info = {}

    else:
        cards_cashback_info = {}

        card_expenses = expenses_this_month_by_card(current_date, card_numbers, xlsx_file)
        for card in card_expenses:
            cards_cashback_info[card] = round(card_expenses[card] / 100, 2)

    return cards_cashback_info


def get_top_five_transactions(current_date: datetime.datetime, xlsx_file: str = op_xlsx) -> List[Any]:
    """Возвращает топ-5 операций по сумме платежа за период с первого числа текущего месяца по текущее число."""

    tr_this_month = get_data_this_month(current_date, xlsx_file)

    if not list(tr_this_month):
        top_tr_inf = []

    else:
        top_tr_abs = sorted([abs(t) for t in list(tr_this_month['Сумма платежа'])], reverse=True)
        top_five_tr = [t for t in list(tr_this_month['Сумма платежа']) if abs(t) in top_tr_abs[:5]]
        top_tr = tr_this_month.loc[tr_this_month['Сумма платежа'].isin(top_five_tr)]

        tr_inf = top_tr.loc[:, ['Дата платежа', 'Сумма платежа', 'Категория', 'Описание']].to_dict(orient='records')

        top_tr_inf = []

        for tr in tr_inf:
            info = {}
            info['date'] = tr.get('Дата платежа')
            info['amount'] = tr.get('Сумма платежа')
            info['category'] = tr.get('Категория')
            info['description'] = tr.get('Описание')
            top_tr_inf.append(info)

    return top_tr_inf


def get_data_in_period(current_date: datetime.datetime, period: str = "M", xlsx_file: str = op_xlsx) -> pd.DataFrame:
    """Возвращает DataFrame с данными о банковских операциях за указанный период.
        Если переиод не указан, то за текущий месяц."""

    try:
        excel_data = pd.read_excel(xlsx_file)
        current_month = current_date.strftime('%m.%Y')
        current_year = str(current_date.year)

    except FileNotFoundError:
        tr_in_period = pd.DataFrame({})

    except AttributeError:
        tr_in_period = pd.DataFrame({})

    else:
        # Даты всех операций:
        tr_dates = list(excel_data['Дата операции'])

        # Даты операций в выбранный период:
        if period == 'M':
            tr_dates_current_month = [d for d in tr_dates if current_month in d]

        elif period == 'W':
            d = current_date.weekday()
            delta = datetime.timedelta(days=d + 1)
            monday = current_date - delta

            tr_dates_current_month = [d for d in tr_dates if datetime.datetime.strptime(d[:10], '%d.%m.%Y') >= monday]

        elif period == 'Y':
            tr_dates_current_month = [d for d in tr_dates if current_year in d]

        elif period == 'ALL':
            tr_dates_current_month = tr_dates

        # Операции в заданный период:
        tr_in_period = excel_data.loc[excel_data['Дата операции'].isin(tr_dates_current_month)]

    return tr_in_period


def total_expenses_in_period(current_date: datetime.datetime, period: str, xlsx_file: str = op_xlsx) -> Dict:
    """Возвращет сумму раходов за указанный период"""

    tr_in_period = get_data_in_period(current_date, period, xlsx_file)

    if not list(tr_in_period):
        total_expenses = {}

    else:
        total_expenses = {'total_amount': round(abs(sum([t for t in list(tr_in_period['Сумма платежа']) if t < 0])))}

    return total_expenses


def expenses_by_category(current_date: datetime.datetime, period: str, xlsx_file: str = op_xlsx) -> List:
    """Возвращает данные по 7 категориям с наибольшими тратами,
    траты по остальным категориям суммируются и попадают в категорию «Остальное»"""

    tr_in_period = get_data_in_period(current_date, period, xlsx_file)

    if not list(tr_in_period):
        top_expenses_categories = [{}]

    else:

        spending_categories = set(tr_in_period['Категория'])

        expenses_categories = {}

        for c in spending_categories:
            gr_by_category = tr_in_period.loc[(tr_in_period['Категория'] == c) & (tr_in_period['Сумма платежа'] < 0)]
            spending_in_category = sum(list(gr_by_category['Сумма платежа']))
            expenses_categories[c] = spending_in_category

        category_sort = sorted(expenses_categories.items(), key=lambda i: i[1])

        top_expenses_categories = []

        for c in category_sort[:7]:
            top_expenses = {}
            top_expenses['category'] = c[0]
            top_expenses['amount'] = round(abs(c[1]))
            top_expenses_categories.append(top_expenses)

        other_spending = []
        for c in category_sort[7:]:
            other_spending.append(c[1])

        top_expenses_categories.append({'Остальное': round(abs(sum(other_spending)))})

    return top_expenses_categories


def get_transfers_and_cash(current_date: datetime.datetime, period: str = 'M', xlsx_file: str = op_xlsx) -> List:
    """Возвращает сумму расходов по категориям «Наличные» и «Переводы» (сортировка по убыванию)"""

    tr_in_period = get_data_in_period(current_date, period, xlsx_file)

    if not list(tr_in_period):
        transfers_and_cash = {}

    else:

        transfers = tr_in_period.loc[(tr_in_period['Категория'] == 'Наличные') & (tr_in_period['Сумма платежа'] < 0)]
        transfers_total = round(abs(sum(list(transfers['Сумма платежа']))))

        cash = tr_in_period.loc[(tr_in_period['Категория'] == 'Переводы') & (tr_in_period['Сумма платежа'] < 0)]
        cash_total = round(abs(sum(list(cash['Сумма платежа']))))

        transfers_and_cash = []

        if cash_total > transfers_total:

            cash = {}
            cash['category'] = 'Наличные'
            cash['amount'] = cash_total
            transfers_and_cash.append(cash)

            transfers = {}
            transfers['category'] = 'Переводы'
            transfers['amount'] = transfers_total
            transfers_and_cash.append(transfers)

        else:
            transfers = {}
            transfers['category'] = 'Переводы'
            transfers['amount'] = transfers_total
            transfers_and_cash.append(transfers)

            cash = {}
            cash['category'] = 'Наличные'
            cash['amount'] = cash_total
            transfers_and_cash.append(cash)

    return transfers_and_cash


def get_total_income_in_period(current_date: datetime.datetime, period: str = 'M', xlsx_file: str = op_xlsx) -> Dict:
    """Возвращет сумму поступлений за указанный период"""

    tr_in_period = get_data_in_period(current_date, period, xlsx_file)

    if not list(tr_in_period):
        total_income = {}

    else:
        total_income = {'total_amount': round(abs(sum([t for t in tr_in_period['Сумма платежа'] if t > 0])))}

    return total_income


def get_income_by_category(current_date: datetime.datetime, period: str = 'M', xlsx_file: str = op_xlsx) -> List:
    """Возвращает список поступлений по категориям (отсортирован по убыванию)"""

    tr_in_period = get_data_in_period(current_date, period, xlsx_file)

    if not list(tr_in_period):
        top_income_categories = [{}]

    else:

        spending_categories = set(tr_in_period['Категория'])

        expenses_categories = {}

        for c in spending_categories:
            gr_by_category = tr_in_period.loc[(tr_in_period['Категория'] == c) & (tr_in_period['Сумма платежа'] > 0)]
            spending_in_category = sum(list(gr_by_category['Сумма платежа']))
            expenses_categories[c] = spending_in_category

        category_sort = sorted(expenses_categories.items(), key=lambda i: i[1], reverse=True)

        top_income_categories = []

        for c in category_sort:
            income_categories = {}
            if c[1] != 0:
                income_categories['category'] = c[0]
                income_categories['amount'] = round(abs(c[1]))
                top_income_categories.append(income_categories)

    return top_income_categories


def get_exchange_rate(currency: Optional[dict] = None) -> Dict:
    """Возвращает текущий курс вылют"""

    if currency is None:
        currency = user_settings['user_currencies']
    exchange_rate = {}

    for c in currency:

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={c}&amount=1"
        response = json.loads(requests.get(url, headers={"apikey": currency_exchange_api}).text)

        result = float(response["info"]["rate"])
        exchange_rate[c] = round(result, 2)

    return exchange_rate


def get_stock_price(current_date: datetime.datetime, stock_symbols: Optional[dict] = None) -> List:
    """Возвращает курс акций на момент запроса"""

    delta = datetime.timedelta(hours=8)

    est_time = (current_date - delta).strftime('%Y-%m-%d %H:%M:00')

    if int((current_date - delta).strftime('%H')) >= 20:
        est_time = (current_date - delta).strftime('%Y-%m-%d 19:59:00')

    elif int((current_date - delta).strftime('%H')) < 10:
        delta = datetime.timedelta(days=1)
        est_time = (current_date - delta).strftime('%Y-%m-%d 19:59:00')

    if stock_symbols is None:
        stock_symbols = user_settings['user_stocks']

    stock_exchange_rate = []

    for s in stock_symbols:
        function = 'TIME_SERIES_INTRADAY'
        url = f'https://www.alphavantage.co/query?function={function}&symbol={s}&interval=1min&apikey={st_api}'
        stock_data = json.loads(requests.get(url).text)
        stock_time = stock_data.get('Time Series (1min)')
        stock_price = stock_time[est_time]

        stock_info = {}

        stock_info['stock'] = s
        stock_info['price'] = round(float(stock_price.get('4. close')), 2)

        stock_exchange_rate.append(stock_info)

    return stock_exchange_rate


def get_transactions_from_excel(xlsx_file: str = op_xlsx):
    """Возвращает DataFrame из Excel-файла"""

    excel_data = pd.read_excel(xlsx_file)

    return excel_data


def get_transactions_dict(xlsx_file: str = op_xlsx):
    """Возвращает список словарей, содержащий информацию о транзакциях:
        Дата операции ('YYYY-MM-DD') и Сумма операции (число)"""

    try:
        excel_data = pd.read_excel(xlsx_file)

        tr_dates = list(excel_data['Дата операции'])

        transactions_list = []

        for date in tr_dates:
            tr_amount = excel_data.loc[excel_data['Дата операции'] == date]
            amount = (list(tr_amount['Сумма платежа']))
            tr_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
            date = tr_date.strftime('%Y-%m-%d')
            date_amount = {date: amount[0]}
            transactions_list.append(date_amount)

    except FileNotFoundError:
        transactions_list = pd.DataFrame([])

    except AttributeError:
        transactions_list = pd.DataFrame([])

    else:
        # Даты всех операций:
        tr_dates = list(excel_data['Дата операции'])

        transactions_list = []

        for date in tr_dates:
            tr_amount = excel_data.loc[excel_data['Дата операции'] == date]
            amount = (list(tr_amount['Сумма платежа']))
            tr_date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
            date = tr_date.strftime('%Y-%m-%d')
            date_amount = {date: amount[0]}
            transactions_list.append(date_amount)

    return transactions_list
