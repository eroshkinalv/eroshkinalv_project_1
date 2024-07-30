import datetime
import json
import logging
from typing import Any, Dict, List

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_transactions_dict, get_transactions_from_excel

xlsx_data = get_transactions_from_excel()

current_date_and_time = datetime.datetime.now()

logging.basicConfig(filename=r'..\log\services.log', encoding='utf-8',
                    filemode='a',
                    format='%(asctime)s, %(filename)s, %(funcName)s, %(levelname)s: %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def cashback_offers(year: str, month: str, data: pd.DataFrame = xlsx_data) -> str:
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
