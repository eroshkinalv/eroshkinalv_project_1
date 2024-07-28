# Проект eroshkinalv_project_1

## Описание:

Проект eroshkinalv_project_1 - это учебный проект на Python, который представляет собой приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.
Проект содержит генераторы для обработки массивов транзакций. Эти генераторы должны позволять пользователям быстро и удобно находить нужную информацию о транзакциях и проводить анализ данных.
В проект добавлен декоратор log, который будет логировать вызов функций-обработчиков и результаты их работы. Это поможет отслеживать работу системы и быстро реагировать на возможные ошибки.
Программа обрабатывает данные о финансовых транзакциях, полученные из XLSX-файлов.

## Структура проекта

1. Веб-страницы:
- Главная
- События
2. Сервисы:
- Выгодные категории повышенного кешбэка
- Инвесткопилка
- Простой поиск
- Поиск по телефонным номерам
- Поиск переводов физическим лицам
3. Отчеты:
- Траты по категории
- Траты по дням недели
- Траты в рабочий/выходной день

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/eroshkinalv/skypro_eroshkinalv.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

1. Откройте приложение на Вашем устройстве.
2. Введите период для поиска банковских операций.
3. Просмотрите или сохраните данные.

## Документация:

Для получения дополнительной информации обратитесь к [папки с документацией пока нет](README.md).

## Лицензия:

Этот проект лицензирован по [лицензии](LICENSE.txt).

## Тестирование:

Данный проект покрыт юнит-тестами. Для их запуска выполните команду:
```
pytest
```
## Именованные журналы сообщений (Логи)

В модулях views и reports реализована запись логов для отслеживания и устранения ошибок.
