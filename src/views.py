import datetime
import json
import logging

from src.utils import (expenses_by_category, expenses_this_month_by_card, get_card_number, get_cashback_amount,
                       get_exchange_rate, get_income_by_category, get_stock_price, get_top_five_transactions,
                       get_total_income_in_period, get_transfers_and_cash, greeting, total_expenses_in_period)

current_date_and_time = datetime.datetime.now()

logging.basicConfig(filename=r'../log/views.log', encoding='utf-8',
                    filemode='w',
                    format='%(asctime)s, %(filename)s, %(funcName)s, %(levelname)s: %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def homepage(date_and_time: datetime.datetime = current_date_and_time) -> json:
    """Генерирует JSON-ответ для страницы «Главная»."""

    try:

        homepage_data = {'greeting': greeting(date_and_time), 'cards': []}
        logging.info(f'{homepage_data}')

        total_spent = expenses_this_month_by_card(date_and_time, get_card_number())

        cashback_amount = get_cashback_amount(date_and_time, get_card_number())

        for num in get_card_number():
            homepage_data['cards'] = [{'last_digits': num,
                                       'total_spent': "%.2f" % total_spent[num],
                                       'cashback': "%.2f" % cashback_amount[num]}]
        logging.info(f'{homepage_data}')

        homepage_data['top_transactions'] = get_top_five_transactions(date_and_time)
        logging.info(f'{homepage_data}')

        homepage_data['currency_rates'] = [{'currency': k, 'rate': v} for k, v in get_exchange_rate().items()]
        logging.info(f'{homepage_data}')

        homepage_data['stock_prices'] = get_stock_price(date_and_time)
        logging.info(f'{homepage_data}')

        json_response = json.dumps(homepage_data, indent=4, ensure_ascii=False)

        logging.info('JSON-ответ "Главная" успешно сформирован.')

        return json_response

    except Exception:
        logging.error('JSON-ответ "Главная" не сформирован.')

    else:
        logging.info('JSON-ответ "Главная" успешно сформирован.')
        return json_response


def recent_activity(current_date: datetime.datetime = current_date_and_time, period: str = 'M') -> json:
    """Генерирует JSON-ответ для страницы «События»."""

    try:

        total_expenses = total_expenses_in_period(current_date, period)

        recent_actions = {'expenses': total_expenses}

        categories = expenses_by_category(current_date, period)

        recent_actions['expenses']['main'] = categories

        tr_n_cash = get_transfers_and_cash(current_date, period)

        recent_actions['expenses']['transfers_and_cash'] = tr_n_cash

        recent_actions['income'] = get_total_income_in_period(current_date, period)

        recent_actions['income']['main'] = get_income_by_category(current_date, period)

        recent_actions['currency_rates'] = [{'currency': k, 'rate': v} for k, v in get_exchange_rate().items()]

        recent_actions['stock_prices'] = get_stock_price(current_date)

        json_response = json.dumps(recent_actions, indent=4, ensure_ascii=False)

        logging.info('JSON-ответ "События" успешно сформирован.')

        return json_response

    except Exception:
        logging.error('JSON-ответ "События" не сформирован.')

    else:
        logging.info('JSON-ответ "События" успешно сформирован.')
        return json_response


# if __name__ == '__main__':
#     print(homepage())
#     print(recent_activity())
