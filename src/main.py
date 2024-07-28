import datetime
import json

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import cashback_offers, investment_bank, search_by_phone_numbers, search_transfers, simple_search
from src.views import homepage, recent_activity

current_date_and_time = datetime.datetime.now()


def main(request: str) -> json:
    """Функция получает некий JSON-запрос и возвращает JSON-ответ """

    if request == 'homepage':

        views_homepage = homepage(current_date_and_time)

        return views_homepage

    elif request == 'activity':

        views_recent_activity = recent_activity(current_date_and_time, request['period'])

        return views_recent_activity

    elif request == 'cashback':

        services_cashback_offers = cashback_offers(request['year'], request['month'])

        return services_cashback_offers

    elif request == 'investment':

        services_investment = investment_bank(request['month'], request['limit'])

        result = {'investment': services_investment}

        json_response = json.dumps(result, indent=4, ensure_ascii=False)

        return json_response

    elif request == 'search':

        if request['search'] == 'simple':

            search_by_word = simple_search(input('Введите слово для поиска: '))

            return search_by_word

        elif request['search'] == 'phone':

            search_by_phone = search_by_phone_numbers(input('Введите номер для поиска: '))

            return search_by_phone

        elif request['search'] == 'transaction':

            search_transactions = search_transfers()

            return search_transactions

    elif request == 'report':

        if request['report'] == 'category':

            expenses_by_category = spending_by_category(input('Введите категорию: '))

            json_response = json.dumps(expenses_by_category, indent=4, ensure_ascii=False)

            return json_response

        elif request['report'] == 'weekday':

            expenses_by_weekday = spending_by_weekday(input('Введите дату: '))

            json_response = json.dumps(expenses_by_weekday, indent=4, ensure_ascii=False)

            return json_response

        elif request['report'] == 'workday':

            expenses_by_workday = spending_by_workday(input('Введите дату: '))

            json_response = json.dumps(expenses_by_workday, indent=4, ensure_ascii=False)

            return json_response
