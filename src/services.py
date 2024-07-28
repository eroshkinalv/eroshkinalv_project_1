import datetime
import json
import logging
import re
from typing import Any, Dict, List

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_transactions_dict, get_transactions_from_excel

op_xlsx = r'C:\Users\liudo\PycharmProjects\Project1_eroshkinalv\data\operations.xlsx'

current_date_and_time = datetime.datetime.now()

logging.basicConfig(filename=r'C:\Users\liudo\PycharmProjects\Project1_eroshkinalv\log\services.log', encoding='utf-8',
                    filemode='a',
                    format='%(asctime)s, %(filename)s, %(levelname)s: %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def cashback_offers(year: str, month: str, data: pd.DataFrame = op_xlsx) -> str:
    """Считет размер кешбэка, который можно заработать в каждой категории в указанном месяце."""

    date = datetime.datetime.strptime(f'01.{month}.{year}', '%d.%m.%Y')

    delta = date + relativedelta(months=+1)

    tr_in_period = data.loc[(data['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S') < delta)) & (
        data['Дата операции'].map(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S') >= date))]

    categories = list(tr_in_period['Категория'].unique())

    cashback_categories = {}

    for c in categories:
        group_by_category = tr_in_period.loc[(tr_in_period['Категория'] == c) & (tr_in_period['Сумма платежа'] < 0)]
        spending_in_category = sum(list(group_by_category['Сумма платежа']))
        if spending_in_category != 0:
            cashback_categories[c] = round(abs(spending_in_category) / 100, 2)

    sorted_categories = dict(sorted(cashback_categories.items()))

    json_response = json.dumps(sorted_categories, indent=4, ensure_ascii=False)

    logging.info('Кешбек сформирован')

    return json_response


def investment_bank(month: str, limit: int, transactions: List[Dict[str, Any]] = get_transactions_dict()) -> float:
    """Возвращает сумму, которую можно отложить в «Инвесткопилку»."""

    inv_bank = []

    if limit == 10:
        for transaction in transactions:
            for k, v in transaction.items():
                if month in k:
                    amount = abs(v)
                    investment_amount = 10 - (amount % 10)
                    amount += investment_amount
                    inv_bank.append(investment_amount)

    elif limit == 100:
        for transaction in transactions:
            for k, v in transaction.items():
                if month in k:
                    amount = abs(v)
                    investment_amount = 100 - (amount % 100)
                    amount += investment_amount
                    inv_bank.append(investment_amount)

    elif limit == 50:
        for transaction in transactions:
            for k, v in transaction.items():
                if month in k:
                    amount = abs(v)
                    investment_amount = 50 - (amount % 100)

                    if investment_amount < 0:
                        investment_amount = 100 - (amount % 100)
                        amount += investment_amount
                    else:
                        amount += investment_amount

                    inv_bank.append(investment_amount)

    investment = round(sum(inv_bank), 2)

    logging.info('Сумма для пополнения инвесткопилки сформирована')

    return investment


def simple_search(user_input: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими запрос пользователя в описании или категории."""

    search_request = ' '.join(user_input.lower().split())
    tr_data = get_transactions_from_excel()

    search_result = tr_data.loc[(tr_data['Категория'].map(
        lambda x: search_request in str(x).lower())) | (
        tr_data['Описание'].map(lambda x: search_request in str(x).lower()))].to_dict(orient='records')

    json_response = json.dumps(search_result, indent=4, ensure_ascii=False)

    logging.info('Ответ на поисковый запрос сформирован')

    return json_response


def search_by_phone_numbers(user_input: str) -> str:
    """Возвращает JSON-ответ со всеми транзакциями, содержащими номер телефона в описании."""

    search_request = user_input
    ph_n = ''.join([num for num in search_request if num not in [' ', '-', '+']])

    tr_data = get_transactions_from_excel()
    data_search = list(tr_data['Описание'])

    search_number = f'+7 {ph_n[-10:-7]} {ph_n[-7:-4]}-{ph_n[-4:-2]}-{ph_n[-2:]}'

    kw = []

    for data in data_search:
        if search_number in str(data).lower():
            kw.append(data)

    s_result = tr_data.loc[tr_data['Описание'].isin(kw)].to_dict(orient='records')

    json_response = json.dumps(s_result, indent=4, ensure_ascii=False)

    logging.info('Ответ на поисковый запрос сформирован')

    return json_response


def search_transfers() -> json:
    """Возвращает JSON-ответ со всеми транзакциями из категории «Переводы»."""

    tr_data = get_transactions_from_excel()
    s_result = tr_data.loc[(tr_data['Категория'] == 'Переводы')].to_dict(orient='records')

    pattern = r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][.]'

    result = []

    for res in s_result:
        search = re.search(pattern, res['Описание'], flags=re.I)
        if search is not None:
            result.append(res)

    json_response = json.dumps(result, indent=4, ensure_ascii=False)

    logging.info('Ответ на поисковый запрос сформирован')

    return json_response
