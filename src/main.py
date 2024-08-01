import datetime
import json

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import cashback_offers, investment_bank
from src.views import homepage, recent_activity

current_date_and_time = datetime.datetime.now()


def main(json_request: str) -> json:
    """Функция получает некий JSON-запрос и возвращает JSON-ответ """

    with open(json_request, 'r', encoding='utf-8') as file:
        request = json.load(file)

    if request['page'] == 'homepage':

        views_homepage = homepage(current_date_and_time)

        return views_homepage

    elif request['page'] == 'activity':

        views_recent_activity = recent_activity(current_date_and_time, request['period'])

        return views_recent_activity

    elif request['page'] == 'cashback':

        services_cashback_offers = cashback_offers(request['year'], request['month'])

        return services_cashback_offers

    elif request['page'] == 'investment':

        services_investment = investment_bank(request['month'], request['limit'])

        result = {'investment': services_investment}

        json_response = json.dumps(result, indent=4, ensure_ascii=False)

        return json_response

    elif request['page'] == 'report':

        if request['report'] == 'category':

            expenses_by_category = spending_by_category(input('Введите категорию: '))

            json_response = expenses_by_category.to_json(orient='records', force_ascii=False)

            return json_response

        elif request['report'] == 'weekday':

            expenses_by_weekday = spending_by_weekday(input('Введите дату: '))

            json_response = expenses_by_weekday.to_json(orient='records', force_ascii=False)

            return json_response

        elif request['report'] == 'workday':

            expenses_by_workday = spending_by_workday(input('Введите дату: '))

            json_response = expenses_by_workday.to_json(orient='records')

            return json_response
