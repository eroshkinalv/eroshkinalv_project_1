import datetime
from typing import Optional
from log.logging import log
import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_transactions_from_excel

current_date_and_time = datetime.datetime.now()
date_and_time = current_date_and_time.strftime('%d.%m.%Y')

tr_data = get_transactions_from_excel()


@log('report_weekday')
def spending_by_weekday(date: Optional[str] = None, transactions: pd.DataFrame = tr_data) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""

    if date is None:
        tr_date = date_and_time
    else:
        tr_date = date

    date_f = datetime.datetime.strptime(tr_date, '%d.%m.%Y')
    delta = date_f + relativedelta(months=-3)

    tr_three_months = transactions.loc[(transactions['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S') >= delta)) & (
        transactions['Дата операции'].map(lambda x: datetime.datetime.strptime(
            x, '%d.%m.%Y %H:%M:%S') <= date_f))].to_dict(orient='records')

    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []

    for tr in tr_three_months:

        date = tr['Дата операции']
        date_f = datetime.datetime.strptime(str(date), '%d.%m.%Y %H:%M:%S')

        if date_f.weekday() == 0 and tr['Сумма платежа'] < 0:
            monday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 1 and tr['Сумма платежа'] < 0:
            tuesday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 2 and tr['Сумма платежа'] < 0:
            wednesday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 3 and tr['Сумма платежа'] < 0:
            thursday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 4 and tr['Сумма платежа'] < 0:
            friday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 5 and tr['Сумма платежа'] < 0:
            saturday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 6 and tr['Сумма платежа'] < 0:
            sunday.append(tr['Сумма платежа'])

    avg_per_weekday = {}

    if monday:
        avg_per_weekday['Понедельник'] = round(sum(monday) / len(monday))
    elif tuesday:
        avg_per_weekday['Вторник'] = round(sum(tuesday) / len(tuesday))
    elif wednesday:
        avg_per_weekday['Среда'] = round(sum(wednesday) / len(wednesday))
    elif thursday:
        avg_per_weekday['Четверг'] = round(sum(thursday) / len(thursday))
    elif friday:
        avg_per_weekday['Пятница'] = round(sum(friday) / len(friday))
    elif saturday:
        avg_per_weekday['Суббота'] = round(sum(saturday) / len(saturday))
    elif sunday:
        avg_per_weekday['Воскресенье'] = round(sum(sunday) / len(sunday))

    df = pd.DataFrame(avg_per_weekday)

    return df


@log('report_category')
def spending_by_category(category: str,
                         transactions: pd.DataFrame = tr_data,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты(DD.MM.YYYY))"""

    if date is None:
        tr_date = date_and_time
    else:
        tr_date = date

    date_f = datetime.datetime.strptime(tr_date, '%d.%m.%Y')
    delta = date_f + relativedelta(months=-3)

    tr_three_months = transactions.loc[(transactions['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S') >= delta)) & (
        transactions['Дата операции'].map(lambda x: datetime.datetime.strptime(
            x, '%d.%m.%Y %H:%M:%S') <= date_f))].to_dict(orient='records')

    sp_by_list = []

    for tr in tr_three_months:
        if tr['Категория'] == category and tr['Сумма платежа'] < 0:
            sp_by_list.append(tr['Сумма платежа'])

    sp_sum = {category: round(sum(sp_by_list))}

    df = pd.DataFrame(sp_sum)

    return df


@log()
def spending_by_workday(date: Optional[str] = None, transactions: pd.DataFrame = tr_data) -> pd.DataFrame:
    """Возвращает средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)"""

    if date is None:
        tr_date = date_and_time
    else:
        tr_date = date

    date_f = datetime.datetime.strptime(tr_date, '%d.%m.%Y')
    delta = date_f + relativedelta(months=- 3)

    tr_three_months = transactions.loc[(transactions['Дата операции'].map(
        lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S') >= delta)) & (
        transactions['Дата операции'].map(lambda x: datetime.datetime.strptime(
            x, '%d.%m.%Y %H:%M:%S') <= date_f))].to_dict(orient='records')

    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []

    for tr in tr_three_months:

        date = tr['Дата операции']
        date_f = datetime.datetime.strptime(str(date), '%d.%m.%Y %H:%M:%S')

        if date_f.weekday() == 0 and tr['Сумма платежа'] < 0:
            monday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 1 and tr['Сумма платежа'] < 0:
            tuesday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 2 and tr['Сумма платежа'] < 0:
            wednesday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 3 and tr['Сумма платежа'] < 0:
            thursday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 4 and tr['Сумма платежа'] < 0:
            friday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 5 and tr['Сумма платежа'] < 0:
            saturday.append(tr['Сумма платежа'])
        elif date_f.weekday() == 6 and tr['Сумма платежа'] < 0:
            sunday.append(tr['Сумма платежа'])

    avg_per_weekday = {}

    mon_to_fri = monday + tuesday + wednesday + thursday + friday
    if len(mon_to_fri) != 0:
        avg_per_weekday['Будни'] = round(sum(mon_to_fri) / len(mon_to_fri))

    if len(saturday + sunday) != 0:
        avg_per_weekday['Выходные'] = round(sum(saturday + sunday) / len(saturday + sunday))

    df = pd.DataFrame(avg_per_weekday)

    return df
